"""Narracion TTS, vo.json y recorte vertical para shorts."""
import json
import re
import sys
from pathlib import Path

from pipe_core import (BASE, HERE, _audio_path, _guardar_log,
                       _narracion_guion, _probe_duration, find_script, fmt_eta,
                       run, Progreso)
from pipe_storyboard import _campo, _narracion_job, _parse_storyboard

def run_tts(job_dir, voice="edge:es-MX-DaliaNeural", language="es",
            progress=None):
    """Lee jobs/<slug>/vo.json ([{id, text}]) y genera audio/<id>.mp3.

    La voz es un spec "<motor>:<voz>" (ver tts_engine.py): edge neural
    (default, la más humana), kokoro local, piper local o hatch legacy.
    progress(stage, done, total, detalle): callback opcional de avance.
    """
    job = Path(job_dir)
    vo_file = job / "vo.json"
    if not vo_file.exists():
        return False, (f"No existe {vo_file}. Crea vo.json con "
                       '[{"id": "s01", "text": "..."}] — un objeto por escena.')
    items = json.loads(vo_file.read_text(encoding="utf-8"))
    if not items:
        return False, f"{vo_file} está vacío."
    sys.path.insert(0, str(HERE))
    import tts_engine
    return tts_engine.speak_batch(items, voice, job / "audio", language,
                                  progress=progress)


# ---------- vo.json automático (desde storyboard o guion) ----------
def _bloque_crudo(job, sid):
    """Devuelve el markdown crudo del bloque de una escena (para diagnóstico).
    v27: cuando una escena no tiene VOZ legible, el error muestra este texto
    para ver el formato real que usó el modelo."""
    sb = Path(job) / "STORYBOARD.md"
    if not sb.exists():
        return ""
    text = sb.read_text(encoding="utf-8", errors="replace")
    sid_u = str(sid).upper()
    m = re.search(rf"(?ms)^###\s*{sid_u}\b(.*?)(?=^###\s*S\d+|\Z)", text)
    return m.group(0).strip()[:600] if m else ""


def build_vo_json(p, job):
    """Crea vo.json ([{id, text}]) desde STORYBOARD.md; si no hay, del guion.

    Devuelve (n_items, origen, sin_voz). v27: las escenas SIN VOZ legible ya
    NO se descartan en silencio (eso causaba un loop infinito: la reparación
    sincronizaba vo.json una y otra vez con menos líneas, el TTS omitía todo
    y el ensamblado seguía fallando). Ahora se reportan en sin_voz para que
    la etapa falle fuerte con la lista exacta.
    """
    items, sin_voz = [], []
    sb = job / "STORYBOARD.md"
    if sb.exists():
        text = sb.read_text(encoding="utf-8", errors="replace")
        guion = _narracion_job(job)
        for m in re.finditer(r"###\s*(S\d+)(.*?)(?=###\s*S\d+|\Z)", text, re.S):
            voz = _campo(m.group(2), "VOZ", guion)
            sid = m.group(1).lower()
            if voz:
                items.append({"id": sid, "text": voz})
            else:
                sin_voz.append(sid)
    if not items:
        sp = find_script(p)
        if sp:
            raw = Path(sp).read_text(encoding="utf-8", errors="replace")
            # v29.1: sin el markup de producción (ver _narracion_guion).
            raw = _narracion_guion(raw)
            paras = [q.strip() for q in raw.split("\n") if len(q.strip()) > 40]
            chunks = []
            for para in paras:
                words = para.split()
                while len(words) > 38:
                    chunks.append(" ".join(words[:38]))
                    words = words[38:]
                if words:
                    chunks.append(" ".join(words))
            items = [{"id": f"s{i + 1:02d}", "text": c}
                     for i, c in enumerate(chunks)]
    if items:
        # v29.1: dedupe de ids repetidos (S41/S42 del proyecto 35: el modelo
        # repitió una escena). Se conserva la primera aparición para no narrar
        # dos veces ni pisar el mismo mp3.
        vistos, uniq = set(), []
        for it in items:
            if it["id"] in vistos:
                continue
            vistos.add(it["id"])
            uniq.append(it)
        items = uniq
        (job / "vo.json").write_text(
            json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
        return len(items), ("storyboard" if sb.exists() else "guion"), sin_voz
    return 0, "", sin_voz


def run_tts_stage(p, job, progress=None):
    extra = ""
    # Sincronía vo.json ↔ storyboard: si el storyboard creció después del
    # TTS (p. ej. "Continuar storyboard" agregó S48), vo.json queda viejo y
    # la escena nueva nunca recibe audio -> el ensamblado falla con
    # "Falta el audio de S48". Se reconstruye si los ids no coinciden.
    sb_ids = [s["id"] for s in _parse_storyboard(job)]
    vf = job / "vo.json"
    vo_ids = []
    if vf.exists():
        try:
            vo_ids = [str(it.get("id", "")).lower()
                      for it in json.loads(vf.read_text(encoding="utf-8"))]
        except Exception:
            vo_ids = []
    if not vf.exists() or (sb_ids and set(sb_ids) != set(vo_ids)):
        n, origen, sin_voz = build_vo_json(p, job)
        if not n:
            return (False, "Sin vo.json ni storyboard/guion para crearlo. "
                           "Genera primero el storyboard (etapa 5).", [], None)
        # v27: escenas sin VOZ legible -> fallar FUERTE con la lista y una
        # muestra del formato real. No en silencio (eso causaba el loop S34:
        # vo.json con menos líneas -> TTS omite -> ensamblado falla). El
        # contrato de la etapa 5 también exige 0 escenas sin VOZ, así que no
        # tiene sentido narrar un storyboard que va a quedar bloqueado.
        if sin_voz:
            muestra = _bloque_crudo(job, sin_voz[0])
            lista = ", ".join(s.upper() for s in sin_voz[:12])
            if len(sin_voz) > 12:
                lista += f" (+{len(sin_voz) - 12} más)"
            return (False,
                    f"El storyboard tiene {len(sin_voz)} escenas sin VOZ "
                    f"legible: {lista}.\n"
                    "El modelo las escribió con un formato que no reconozco "
                    "(cada escena necesita una línea 'VOZ: ...'). Muestra de "
                    f"la primera ({sin_voz[0].upper()}):\n---\n{muestra}\n---\n"
                    "Edita STORYBOARD.md y dales formato 'VOZ: ...' / "
                    "'VISUAL: ...', o re-ejecuta la etapa 5 (Storyboard). "
                    "Cuando las arregles, re-ejecuta esta etapa.",
                    [], None)
        extra = f"vo.json sincronizado desde {origen} ({n} líneas). "
    ok, log = run_tts(job, p["voice"], p["language"], progress=progress)
    # v26 — verificación posterior ESTRUCTURAL: el TTS omite los audios que
    # "ya existen", pero si un archivo se corrompió o se borró entre el
    # chequeo y el ensamblado, la etapa 8 fallaba con "Falta el audio de Sxx"
    # aunque la 6 había reportado ok. Ahora la etapa 6 no puede terminar en ok
    # sin que cada escena de vo.json tenga un audio válido (existe, no vacío
    # y con duración legible). Si algo falla, se dice exactamente qué.
    mal = []
    try:
        vitems = json.loads(vf.read_text(encoding="utf-8")) if vf.exists() else []
    except Exception:
        vitems = []
    for it in vitems:
        sid = str(it.get("id", "")).lower()
        au = _audio_path(job, sid)
        if not au.exists() or au.stat().st_size == 0:
            mal.append(f"{sid.upper()} (sin archivo)")
        elif _probe_duration(au) <= 0:
            mal.append(f"{sid.upper()} (ilegible/corrupto)")
    if mal:
        return (False,
                "TTS terminó pero estos audios quedaron inválidos: "
                + ", ".join(mal) + ". Bórralos de audio/ (o usa «Forzar» en "
                  "«🛠 Reparar faltantes») y re-ejecuta la etapa 6.",
                [], None)
    arts = [str(a) for a in (job / "audio").glob("*.mp3")] if ok else []
    full = extra + log
    logf = _guardar_log(job, "tts", [full])
    if logf:
        full += f"\n📄 Log completo de esta ejecución: {logf}"
    return ok, full, arts, None


def _ids_con_archivo(ids, carpeta, ext):
    """De una lista de ids, devuelve (tienen, faltan) según existan archivos
    no vacíos en la carpeta. Los ids se normalizan a minúsculas igual que
    _audio_path (en Windows da igual, pero el log queda consistente)."""
    tienen, faltan = [], []
    for i in ids:
        f = carpeta / f"{str(i).lower()}{ext}"
        if f.exists() and f.stat().st_size > 0:
            tienen.append(i)
        else:
            faltan.append(i)
    return tienen, faltan


# ---------- recorte vertical para shorts (automático) ----------
def cut_vertical(src_mp4, dst_mp4, start, end):
    """Corta [start,end], reencuadra a 1080x1920 y quema subtítulos si hay SRT."""
    src = Path(src_mp4)
    srt = src.with_suffix(".srt")
    vf = ("crop=720:720:(in_w-720)/2:(in_h-720)/2,"  # cuadrado central
          "scale=1080:1080,"
          "pad=1080:1920:0:(1920-1080)/2:black")     # bandas arriba/abajo
    if srt.exists():
        vf += f",subtitles='{srt}':force_style='FontName=Gochi Hand,FontSize=22'"
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-to", str(end),
           "-i", str(src), "-vf", vf,
           "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-c:a", "aac", str(dst_mp4)]
    return run(cmd, timeout=600)


def fmt_mmss(secs):
    m, s = divmod(int(round(secs or 0)), 60)
    return f"{m:02d}:{s:02d}"


def segmento_de_escena(job, sid):
    """(inicio, fin) en segundos de una escena Sxx, desde los audios TTS."""
    vo = job / "vo.json"
    if not vo.exists():
        return None
    try:
        items = json.loads(vo.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None
    t = 0.0
    sid = sid.strip().lower()
    for it in items:
        au = _audio_path(job, it["id"])
        dur = _probe_duration(au) if au.exists() else 0.0
        if it["id"].lower() == sid:
            return (t, t + dur)
        t += dur
    return None


def sugerencia_corto(job):
    """Lee 'SHORT SUGERIDO: Sxx' del PAQUETE.md → (Sxx, t0, t1 en segundos)."""
    paq = job / "PAQUETE.md"
    if not paq.exists():
        return None
    m = re.search(r"SHORT SUGERIDO:\s*(S\d+)",
                  paq.read_text(encoding="utf-8", errors="replace"), re.I)
    if not m:
        return None
    seg = segmento_de_escena(job, m.group(1))
    if not seg:
        return None
    return (m.group(1).upper(), seg[0], seg[1])


# ---------- dispatcher de etapas ----------
