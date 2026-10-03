#!/usr/bin/env python3
"""Runner TTS del panel Zenn Factory (proceso aparte, un lote por etapa).

Uso:  python tts_runner.py <lote.json>
Lote: {"engine": "...", "voice": "...", "language": "es",
       "items": [{"id": "s01", "text": "...", "out": "ruta.mp3"}]}
Imprime al final UNA línea JSON: {"ok": [ids], "fail": {id: error}}

Motores:
  edge   edge-tts (Microsoft neural, gratis, internet)
  kokoro Kokoro-82M local (pip: kokoro, soundfile; sistema: espeak-ng)
  piper  Piper local (pip: piper-tts; descarga la voz sola la 1ª vez)
  hatch  /opt/hatch/bin/tts (legacy)

Al final normaliza cada mp3 con ffmpeg loudnorm (I=-16) si hay ffmpeg:
volumen consistente = menos "sonido IA".
"""
import asyncio
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def normalize(mp3):
    """loudnorm a -16 LUFS, en sitio, si hay ffmpeg."""
    if not shutil.which("ffmpeg"):
        return
    tmp = mp3.with_suffix(".norm.mp3")
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(mp3),
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100",
         str(tmp)], capture_output=True, text=True)
    if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
        tmp.replace(mp3)
    elif tmp.exists():
        tmp.unlink()


def gen_edge(items, voice, rate="+0%"):
    import edge_tts

    async def one(it):
        comm = edge_tts.Communicate(it["text"], voice, rate=rate)
        await comm.save(it["out"])

    async def run_all():
        for it in items:
            try:
                await one(it)
                ok.append(it["id"])
            except Exception as e:
                try:  # un reintento: el endpoint a veces corta
                    await one(it)
                    ok.append(it["id"])
                except Exception as e2:
                    fail[it["id"]] = str(e2)[:200]
    asyncio.run(run_all())


def gen_kokoro(items, voice):
    import soundfile as sf
    from kokoro import KPipeline
    pipe = KPipeline(lang_code="e")
    for it in items:
        try:
            chunks = []
            for _, _, audio in pipe(it["text"], voice=voice):
                chunks.append(audio)
            if not chunks:
                raise RuntimeError("sin audio generado")
            import numpy as np
            full = np.concatenate(chunks)
            with tempfile.NamedTemporaryFile(suffix=".wav",
                                             delete=False) as tf:
                wav = tf.name
            sf.write(wav, full, 24000)
            r = subprocess.run(
                ["ffmpeg", "-v", "error", "-y", "-i", wav,
                 "-codec:a", "libmp3lame", "-q:a", "2", it["out"]],
                capture_output=True, text=True)
            Path(wav).unlink(missing_ok=True)
            if r.returncode != 0:
                raise RuntimeError(r.stderr[-200:])
            ok.append(it["id"])
        except Exception as e:
            fail[it["id"]] = str(e)[:200]


def gen_piper(items, voice):
    vdir = HERE / "piper_voices"
    vdir.mkdir(parents=True, exist_ok=True)
    model = vdir / f"{voice}.onnx"
    if not model.exists():
        r = subprocess.run(
            [sys.executable, "-m", "piper.download_voices", voice,
             "--download-dir", str(vdir)],
            capture_output=True, text=True, timeout=600)
        if not model.exists():
            raise RuntimeError(
                f"No pude descargar la voz piper {voice}: "
                f"{(r.stderr or '')[-200:]}")
    for it in items:
        try:
            with tempfile.NamedTemporaryFile(
                    suffix=".txt", delete=False, mode="w",
                    encoding="utf-8") as tf:
                tf.write(it["text"])
                txt = tf.name
            wav = txt + ".wav"
            r = subprocess.run(
                [sys.executable, "-m", "piper", "--model", str(model),
                 "--input_file", txt, "--output_file", wav],
                capture_output=True, text=True, timeout=300)
            if r.returncode != 0:
                raise RuntimeError(r.stderr[-200:])
            r = subprocess.run(
                ["ffmpeg", "-v", "error", "-y", "-i", wav,
                 "-codec:a", "libmp3lame", "-q:a", "2", it["out"]],
                capture_output=True, text=True)
            Path(txt).unlink(missing_ok=True)
            Path(wav).unlink(missing_ok=True)
            if r.returncode != 0:
                raise RuntimeError(r.stderr[-200:])
            ok.append(it["id"])
        except Exception as e:
            fail[it["id"]] = str(e)[:200]


def gen_hatch(items, voice, language):
    binary = "/opt/hatch/bin/tts"
    if not Path(binary).exists():
        raise RuntimeError("El motor hatch no existe en esta máquina.")
    for it in items:
        p = subprocess.run(
            [binary, "speak", "--voice", voice, "--language", language,
             "--output", it["out"], "--text-stdin"],
            input=it["text"].encode(), capture_output=True, timeout=300)
        if p.returncode == 0 and Path(it["out"]).exists():
            ok.append(it["id"])
        else:
            fail[it["id"]] = (p.stderr or b"").decode(errors="replace")[-200:]


ok, fail = [], {}
batch = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
engine, voice = batch["engine"], batch["voice"]
items = batch["items"]
try:
    if engine == "edge":
        gen_edge(items, voice)
    elif engine == "kokoro":
        gen_kokoro(items, voice)
    elif engine == "piper":
        gen_piper(items, voice)
    elif engine == "hatch":
        gen_hatch(items, voice, batch.get("language", "es"))
    else:
        raise RuntimeError(f"Motor desconocido: {engine}")
except Exception as e:
    for it in items:
        if it["id"] not in ok:
            fail[it["id"]] = str(e)[:200]

for it in items:
    if it["id"] in ok:
        p = Path(it["out"])
        if p.exists() and p.stat().st_size > 0:
            normalize(p)
        else:
            ok.remove(it["id"])
            fail[it["id"]] = "archivo vacío"

print(json.dumps({"ok": ok, "fail": fail}, ensure_ascii=False))
