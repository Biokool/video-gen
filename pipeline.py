#!/usr/bin/env python3
"""Definición del pipeline y ejecutores de etapa del panel Zenn Factory.

Etapas video largo (10):
  tema -> investigacion -> guion -> verificacion -> storyboard ->
  tts -> animacion -> ensamblado -> miniatura -> paquete

Etapas corto-recorte (a partir de un largo publicado):
  seleccion -> recorte -> subtitulos -> paquete

Etapas corto-standalone (guion propio de 30-60s):
  guion -> tts -> animacion -> ensamblado -> paquete (vertical)

Cada etapa declara si es automática (hook implementado), asistida (usa LLM)
o manual (se marca completada a mano). Nada finge: lo no implementado se
declara manual en el panel.
"""
import re
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent  # ~/workspace/zenn-factory

STAGES_LARGO = [
    ("tema", "Tema aprobado", "manual"),
    ("investigacion", "Investigación + fuentes", "asistida"),
    ("guion", "Guion (borrador + crítico)", "asistida"),
    ("verificacion", "Verificación de fuentes", "automatica"),
    ("storyboard", "Storyboard", "asistida"),
    ("tts", "Narración TTS", "automatica"),
    ("animacion", "Animación (Manim)", "manual"),
    ("ensamblado", "Ensamblado + SRT", "automatica"),
    ("miniatura", "Miniaturas", "automatica"),
    ("paquete", "Paquete de publicación", "manual"),
]

STAGES_RECORTE = [
    ("seleccion", "Selección del segmento", "asistida"),
    ("recorte", "Recorte vertical 1080x1920", "automatica"),
    ("subtitulos", "Subtítulos quemados", "automatica"),
    ("paquete", "Paquete del corto", "manual"),
]

STAGES_SHORT = [
    ("guion", "Guion corto (30-60s)", "asistida"),
    ("tts", "Narración TTS", "automatica"),
    ("animacion", "Animación vertical (Manim)", "manual"),
    ("ensamblado", "Ensamblado + SRT", "automatica"),
    ("paquete", "Paquete del corto", "manual"),
]

GATES = ["tema", "guion", "miniatura"]


def stages_for(kind):
    if kind == "corto-recorte":
        return STAGES_RECORTE
    if kind == "corto-standalone":
        return STAGES_SHORT
    return STAGES_LARGO


# ---------- utilidades ----------
def run(cmd, cwd=BASE, timeout=3600):
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True,
                       timeout=timeout)
    log = (p.stdout or "")[-3000:] + (p.stderr or "")[-3000:]
    return p.returncode == 0, log


def count_words(text):
    return len(re.findall(r"[A-Za-zÁÉÍÓÚáéíóúÑñüÜ]+", text))


def estimate_minutes(words, wpm=155):
    return words / wpm


# ---------- verificación de fuentes (automática) ----------
DOI_RE = re.compile(r"10\.\d{4,}/[^\s)\]]+")
PMID_RE = re.compile(r"PMID\s*[: ]\s*(\d+)", re.IGNORECASE)


def extract_references(text):
    dois = sorted(set(DOI_RE.findall(text)))
    pmids = sorted(set(PMID_RE.findall(text)))
    return dois, pmids


# ---------- TTS genérico (automático) ----------
def run_tts(job_dir, voice="avocado_v2:MAI_01", language="es"):
    """Lee jobs/<slug>/vo.json ([{id, text}]) y genera audio/<id>.mp3."""
    job = Path(job_dir)
    vo_file = job / "vo.json"
    if not vo_file.exists():
        return False, f"No existe {vo_file}. Crea vo.json con [{{id, text}}]."
    import json
    items = json.loads(vo_file.read_text(encoding="utf-8"))
    audio_dir = job / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    ok, fails = 0, []
    for it in items:
        out = audio_dir / f"{it['id'].lower()}.mp3"
        p = subprocess.run(
            ["/opt/hatch/bin/tts", "speak", "--voice", voice,
             "--language", language, "--output", str(out), "--text-stdin"],
            input=it["text"].encode(), capture_output=True, cwd=str(BASE),
            timeout=300,
        )
        if p.returncode == 0 and out.exists() and out.stat().st_size > 0:
            ok += 1
        else:
            fails.append(it["id"])
    log = f"TTS {ok}/{len(items)} OK" + (f" | fallos: {fails}" if fails else "")
    return not fails, log


# ---------- miniaturas (automático) ----------
def run_thumbnails():
    return run(["python3", "thumbnails/generate_thumbnails.py"], timeout=300)


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


# ---------- propuestas de temas (asistida por LLM) ----------
TOPIC_PROMPT = """Propón 8 temas para videos de curiosidad científica al estilo del canal de YouTube Zenn:
una sola pregunta por video, 8-12 minutos, animación minimalista de monigotes.
Público: hispanohablantes curiosos, tono claro y directo, sin sensacionalismo.
Para cada tema devuelve EXACTAMENTE este formato, sin texto extra:

PREGUNTA: <la pregunta del video>
ANGULO: <1 línea: por qué engancha>
SENAL: <1 línea: evidencia de interés: búsquedas, tendencia o dato>

Repite el bloque 8 veces."""


def propose_topics(generate_fn, n=8):
    text, model = generate_fn(TOPIC_PROMPT,
                              system="Eres un editor de un canal de divulgación científica.")
    topics = []
    for block in text.split("PREGUNTA:")[1:]:
        q = block.split("ANGULO:")[0].strip()
        rest = block.split("ANGULO:")[1] if "ANGULO:" in block else ""
        angle = rest.split("SEÑAL:")[0].strip() if "SEÑAL:" in rest else rest.strip()
        signal = rest.split("SEÑAL:")[1].strip() if "SEÑAL:" in rest else ""
        if q:
            topics.append({"question": q, "angle": angle,
                           "signals": signal, "source": f"llm:{model}"})
        if len(topics) >= n:
            break
    return topics


# ---------- guion: borrador + crítico (asistida por LLM) ----------
def draft_script(generate_fn, question, prompt_maestro, target_words=1300):
    prompt = (f"{prompt_maestro}\n\nESCRIBE EL GUION COMPLETO para:\n{question}\n\n"
              f"Objetivo: ~{target_words} palabras de narración.")
    text, model = generate_fn(prompt, system="Eres guionista de divulgación científica.")
    return text, model


CRITIC_PROMPT = """Eres el editor crítico de un canal de divulgación. Revisa este guion y responde SOLO con:
1. Palabras de narración (número aproximado).
2. ¿Responde UNA sola pregunta? (sí/no + cuál)
3. Fuentes citadas: ¿parecen reales y verificables? (lista las que dudes)
4. Hook: ¿los primeros 20 segundos enganchan? (1 línea)
5. Fallos concretos a corregir (lista corta, sin rodeos).

GUION:
"""


def critic_review(generate_fn, script_text):
    text, model = generate_fn(CRITIC_PROMPT + script_text,
                              system="Eres un editor exigente y directo.")
    return text, model
