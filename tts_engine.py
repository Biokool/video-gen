#!/usr/bin/env python3
"""Motores de voz (TTS) del panel Zenn Factory.

La voz de un proyecto es un "spec":  "<motor>:<voz>"
  edge:es-MX-DaliaNeural   Microsoft Edge neural — gratis, sin key,
                           MUY natural. Necesita internet.
  kokoro:ef_dora           Kokoro-82M local — natural, sin internet.
                           Requiere: pip install kokoro soundfile
                           + espeak-ng instalado en el sistema.
  piper:es_ES-davefx-medium  Piper local — ligero y rapidísimo en CPU;
                           calidad correcta, algo más robótica.
  hatch:avocado_v2:MAI_01  Motor Meta del entorno Hatch (legacy).

Voces en español, mujer y hombre, México y España.
La generación la hace tts_runner.py en UN solo proceso por etapa
(el modelo local se carga una vez) y normaliza el volumen con
ffmpeg loudnorm — eso solo ya quita mucho "sonido IA plano".
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

VOICE_CATALOG = {
    "edge": {
        "label": "Edge Neural · Microsoft (gratis, internet, la más humana)",
        "voices": [
            ("es-MX-DaliaNeural", "Mujer · México — Dalia (recomendada)"),
            ("es-MX-JorgeNeural", "Hombre · México — Jorge"),
            ("es-ES-ElviraNeural", "Mujer · España — Elvira"),
            ("es-ES-AlvaroNeural", "Hombre · España — Álvaro"),
        ],
    },
    "kokoro": {
        "label": "Kokoro · local 82M (sin internet, natural)",
        "voices": [
            ("ef_dora", "Mujer · España — Dora"),
            ("em_alex", "Hombre · España — Alex"),
            ("em_santa", "Hombre · España — Santa"),
        ],
    },
    "piper": {
        "label": "Piper · local ligero (CPU, el más rápido)",
        "voices": [
            ("es_ES-sharvard-medium", "Mujer · España — Sharvard"),
            ("es_MX-claude-high", "Mujer · México — Claude"),
            ("es_ES-davefx-medium", "Hombre · España — DaveFX"),
            ("es_MX-ald-medium", "Hombre · México — Ald"),
        ],
    },
    "hatch": {
        "label": "Aria · Meta (legacy, solo entorno Hatch)",
        "voices": [("avocado_v2:MAI_01", "Mujer · Aria")],
    },
}

DEFAULT_SPEC = "edge:es-MX-DaliaNeural"
ENGINES = list(VOICE_CATALOG)


def parse_spec(spec):
    """'edge:es-MX-DaliaNeural' -> ('edge', 'es-MX-DaliaNeural').

    Valores legacy sin prefijo se mapean por su forma.
    """
    s = (spec or "").strip()
    if ":" in s:
        eng, voice = s.split(":", 1)
        if eng in VOICE_CATALOG and not voice.startswith("MAI"):
            return eng, voice
        if eng == "avocado_v2":  # spec legacy completo de hatch
            return "hatch", s
    if s.endswith("Neural"):
        return "edge", s
    if s.startswith(("ef_", "em_")):
        return "kokoro", s
    if s.startswith("es_"):
        return "piper", s
    if s.startswith("avocado"):
        return "hatch", s
    return "edge", VOICE_CATALOG["edge"]["voices"][0][0]


def runner_path():
    for c in (HERE / "tts_runner.py", HERE / "panel" / "tts_runner.py"):
        if c.exists():
            return c
    return HERE / "tts_runner.py"


def speak_batch(items, spec, audio_dir, language="es", progress=None):
    """Genera audio/<id>.mp3 para [{id, text}]. Devuelve (ok, log).

    Kokoro carga el modelo una vez: va en un solo lote. Los demás
    motores van elemento por elemento para reportar avance real.
    progress(stage, done, total, detalle): callback opcional.
    """
    engine, voice = parse_spec(spec)
    audio_dir = Path(audio_dir)
    audio_dir.mkdir(parents=True, exist_ok=True)

    def run_batch(sub):
        batch = {
            "engine": engine, "voice": voice, "language": language,
            "items": [{"id": it["id"], "text": it["text"],
                       "out": str(audio_dir / f"{it['id'].lower()}.mp3")}
                      for it in sub],
        }
        bfile = audio_dir / "_tts_batch.json"
        bfile.write_text(json.dumps(batch, ensure_ascii=False),
                         encoding="utf-8")
        r = subprocess.run([sys.executable, str(runner_path()), str(bfile)],
                           capture_output=True, text=True, timeout=3600)
        try:
            return json.loads((r.stdout or "").strip().splitlines()[-1])
        except Exception:
            return {"ok": [],
                    "fail": {it["id"]: "El runner TTS no respondió "
                                       f"(motor {engine}). "
                                       f"{(r.stderr or '')[-200:]}"
                             for it in sub}}

    total, ok_ids, fails = len(items), [], {}
    # Reparación: omite los audios que ya existen (no vacíos). Así re-ejecutar
    # la etapa 6 solo genera los faltantes en vez de narrar todo de nuevo.
    pendientes, omitidos = [], 0
    for it in items:
        f = audio_dir / f"{it['id'].lower()}.mp3"
        if f.exists() and f.stat().st_size > 0:
            omitidos += 1
        else:
            pendientes.append(it)
    items = pendientes
    total = len(items)
    if engine == "kokoro":
        if progress:
            progress("tts", 0, total, "cargando modelo Kokoro…")
        res = run_batch(items)
        ok_ids, fails = res.get("ok", []), res.get("fail", {})
        if progress:
            progress("tts", total, total, f"{len(ok_ids)}/{total} audios")
    else:
        for i, it in enumerate(items, 1):
            if progress:
                progress("tts", i - 1, total, f"narrando {it['id'].upper()}")
            res = run_batch([it])
            ok_ids += res.get("ok", [])
            fails.update(res.get("fail", {}))
            if progress:
                progress("tts", i, total,
                         f"{it['id'].upper()} listo" if it["id"] in ok_ids
                         else f"{it['id'].upper()} falló")
    log = (f"TTS motor {engine} · voz {voice}: {len(ok_ids)}/{total} OK"
           + (f" | omitidos (ya existían): {omitidos}" if omitidos else "")
           + (f" | fallos: {fails}" if fails else "")
           + " · volumen normalizado (loudnorm).")
    return not fails, log
