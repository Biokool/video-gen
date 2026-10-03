#!/usr/bin/env python3
"""Definición del pipeline y ejecutores de etapa del panel Zenn Factory.

Etapas video largo (10), EN ESTE ORDEN:
  1 tema -> 2 investigacion -> 3 guion -> 4 verificacion -> 5 storyboard ->
  6 tts -> 7 animacion -> 8 ensamblado -> 9 miniatura -> 10 paquete

Etapas corto-recorte:
  seleccion -> recorte -> subtitulos -> paquete

Etapas corto-standalone:
  guion -> tts -> animacion -> ensamblado -> paquete

Cada etapa declara si es automática, asistida (usa LLM) o manual.
`execute_stage()` devuelve (ok, log, artefactos, estado_sugerido):
el estado sugerido permite, p. ej., que el guion quede 'en-curso'
hasta que el humano lo aprueba en la puerta 1.

`run_all()` ejecuta en orden y se detiene donde hace falta un humano:
puertas de aprobación (guion, miniatura) y etapas manuales.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Dos layouts soportados:
#  - anidado: panel/ dentro de zenn-factory/ (jobs/ y thumbnails/ en el padre)
#  - plano:   todo dentro de video-gen/ (jobs/ y thumbnails/ junto a app.py)
_par = HERE.parent
if HERE.name == "panel" and ((_par / "jobs").exists()
                              or (_par / "PROMPT_MAESTRO.md").exists()):
    BASE = _par
else:
    BASE = HERE

STAGES_LARGO = [
    ("tema", "Tema aprobado", "manual"),
    ("investigacion", "Investigación + fuentes", "asistida"),
    ("guion", "Guion (borrador + crítico)", "asistida"),
    ("verificacion", "Verificación de fuentes", "automatica"),
    ("storyboard", "Storyboard", "asistida"),
    ("tts", "Narración TTS", "automatica"),
    ("animacion", "Animación (Manim)", "asistida"),
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

# Etapas que solo puede completar un humano.
MANUAL_STAGES = {"seleccion"}

# Qué hace cada etapa y qué necesita (se muestra en el panel).
STAGE_HINTS = {
    "tema": "La pregunta del video. Se aprueba en la Bandeja de temas.",
    "investigacion": "El modelo investiga la ciencia del tema y guarda "
                     "INVESTIGACION.md con fuentes reales.",
    "guion": "Genera el borrador con el PROMPT_MAESTRO. Queda en curso "
             "hasta que TÚ lo apruebas en la Puerta 1.",
    "verificacion": "Extrae los DOI/PMID del guion y los lista.",
    "storyboard": "Divide el guion en escenas numeradas (S01...) con su "
                  "descripción visual. Lo guarda en STORYBOARD.md.",
    "tts": "Genera vo.json desde el storyboard (si falta) y narra cada "
           "escena a audio/<id>.mp3 con la voz elegida.",
    "animacion": "El modelo genera el código Manim de cada escena (con el "
                 "rig de monigotes) y lo renderiza a video/scenes/. Si una "
                 "escena falla, intenta repararla solo (máx 2 intentos).",
    "ensamblado": "Une escenas + audios (el audio manda: la imagen se ajusta "
                  "a la voz), genera final.mp4, final.srt y la versión con "
                  "subtítulos quemados.",
    "miniatura": "Genera 3 miniaturas ilustradas según el tema. Elige una "
                 "en la Puerta 2 antes del paquete.",
    "paquete": "Genera PAQUETE.md: título, descripción, capítulos y tags "
               "listos para pegar en YouTube.",
    "seleccion": "Elige el segmento del largo (inicio/fin) en la herramienta "
                 "de recorte de la vista del proyecto.",
    "recorte": "Corta el segmento y lo reencuadra a 1080x1920.",
    "subtitulos": "Quema los subtítulos del SRT en el corto.",
}


def stages_for(kind):
    if kind == "corto-recorte":
        return STAGES_RECORTE
    if kind == "corto-standalone":
        return STAGES_SHORT
    return STAGES_LARGO


def stage_label(kind, stage):
    return dict((s, n) for s, n, _ in stages_for(kind)).get(stage, stage)


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


def pget(p, key, default=None):
    """Lee un campo de un proyecto (dict o sqlite3.Row) sin explotar."""
    try:
        v = p[key]
    except Exception:
        v = None
    return default if v is None else v


def job_dir_of(p):
    jd = pget(p, "job_dir")
    if jd:
        path = Path(jd)
        if not path.is_absolute():
            path = BASE / path
        path.mkdir(parents=True, exist_ok=True)
        return path
    path = BASE / f"jobs/{p['id']}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def find_script(p):
    job = job_dir_of(p)
    for name in ("GUION.md", "GUION_PILOTO.md", "guion.md"):
        c = job / name
        if c.exists():
            return str(c)
    cands = sorted(job.glob("*.md"))
    return str(cands[0]) if cands else ""


DEFAULT_PROMPT_MAESTRO = """Eres guionista de un canal de divulgación científica (estilo Zenn):
- UN video = UNA sola pregunta. Nada de temas dobles.
- Idioma: español claro, frases cortas, tono directo sin sensacionalismo.
- Estructura: hook de 20 segundos que plantee la pregunta -> 5-7 capítulos ->
  cierre que responda la pregunta y deje una idea memorable.
- Cita fuentes reales y verificables (autor, año, DOI/PMID) cuando uses datos.
- La narración se lee en voz alta: escribe para el oído, no para el ojo.
"""


def prompt_maestro():
    p = BASE / "PROMPT_MAESTRO.md"
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    p2 = BASE / "panel" / "PROMPT_MAESTRO.md"
    if p2.exists():
        return p2.read_text(encoding="utf-8", errors="replace")
    return DEFAULT_PROMPT_MAESTRO


# ---------- verificación de fuentes (automática) ----------
DOI_RE = re.compile(r"10\.\d{4,}/[^\s)\]]+")
PMID_RE = re.compile(r"PMID\s*[: ]\s*(\d+)", re.IGNORECASE)


def extract_references(text):
    dois = sorted(set(DOI_RE.findall(text)))
    pmids = sorted(set(PMID_RE.findall(text)))
    return dois, pmids


# ---------- investigación (asistida) ----------
RESEARCH_PROMPT = """Eres el investigador de un canal de divulgación científica (estilo Zenn).
Pregunta del video: "{question}"

Devuelve un informe en español con EXACTAMENTE este formato:
## RESUMEN
5-8 líneas: qué dice la ciencia actual sobre la pregunta.

## FUENTES
3-5 fuentes reales y verificables (autor, año, título; DOI o PMID si existe).

## DATOS CLAVE
- Cifras y datos concretos útiles para el guion (uno por línea).

## ANGULO
1-2 líneas: el ángulo narrativo más atractivo para el video.

No inventes fuentes: si no conoces una fuente real, di "sin fuente verificada".
"""


def run_investigacion(generate_fn, question, job):
    if not generate_fn:
        return (False, "Necesita un backend LLM: configura una key en "
                       "Configuración o usa Ollama local.", [], None)
    try:
        text, model = generate_fn(
            RESEARCH_PROMPT.format(question=question),
            system="Eres un investigador riguroso de divulgación científica.")
    except Exception as e:
        return False, f"Error del modelo: {e}", [], None
    out = job / "INVESTIGACION.md"
    out.write_text(text, encoding="utf-8")
    log = (f"Informe generado con {model} ({len(text)} caracteres).\n"
           f"Guárdalo: es la base del guion. Revísalo antes de aprobar.")
    return True, log, [str(out)], None


# ---------- guion: borrador + crítico (asistida) ----------
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


def run_guion_draft(generate_fn, p, job, kind="largo"):
    if not generate_fn:
        return (False, "Necesita un backend LLM: configura una key en "
                       "Configuración o usa Ollama local.", [], None)
    target = 150 if kind != "largo" else 1300
    research = ""
    inv = job / "INVESTIGACION.md"
    if inv.exists():
        research = ("\n\nINVESTIGACIÓN PREVIA (úsala como base de fuentes):\n"
                    + inv.read_text(encoding="utf-8", errors="replace")[:6000])
    try:
        txt, used = draft_script(
            generate_fn, p["title"],
            prompt_maestro() + research, target_words=target)
    except Exception as e:
        return False, f"Error del modelo: {e}", [], None
    out = job / "GUION.md"
    out.write_text(txt, encoding="utf-8")
    words = count_words(txt)
    log = (f"Borrador con {used}: {words} palabras ≈ "
           f"{estimate_minutes(words):.1f} min.\n"
           "PENDIENTE: léelo abajo y apruébalo en la Puerta 1.")
    # Ojo: estado 'en-curso' — la etapa solo se cierra con tu aprobación.
    return True, log, [str(out)], "en-curso"


# ---------- storyboard (asistida) ----------
STORYBOARD_PROMPT = """Eres director de animación de un canal de divulgación con monigotes minimalistas.
Divide este guion en escenas numeradas. Por escena: el texto de narración LITERAL
y una descripción visual de 1 línea (qué monigote u objeto se ve).

Formato EXACTO por escena:
### S01
VOZ: <texto literal del guion>
VISUAL: <descripción>

GUION:
{script}
"""


def run_storyboard(generate_fn, p, job):
    if not generate_fn:
        return (False, "Necesita un backend LLM: configura una key en "
                       "Configuración o usa Ollama local.", [], None)
    sp = find_script(p)
    if not sp:
        return False, "Sin guion: primero genera el borrador (etapa guion).", [], None
    script = Path(sp).read_text(encoding="utf-8", errors="replace")
    try:
        text, model = generate_fn(
            STORYBOARD_PROMPT.format(script=script[:12000]),
            system="Eres director de animación minimalista.")
    except Exception as e:
        return False, f"Error del modelo: {e}", [], None
    out = job / "STORYBOARD.md"
    out.write_text(text, encoding="utf-8")
    n = text.count("### S")
    return True, f"Storyboard con {model}: {n} escenas en {out}.", [str(out)], None


# ---------- paquete de publicación (asistida) ----------
PAQUETE_PROMPT = """Eres el editor de un canal de YouTube de divulgación científica en español (estilo Zenn).
Genera el paquete de publicación COMPLETO para el video "{title}", con EXACTAMENTE este formato:

TITULOS:
1. <opción 1: máx 60 caracteres, palabra clave al frente, gancho honesto>
2. <opción 2>
3. <opción 3>

DESCRIPCION:
<2 primeras líneas = el gancho: qué se pregunta el video y qué se lleva el espectador (se ven sin desplegar)>
<resumen de 2-3 frases con la palabra clave>

LO QUE VERAS:
- <punto 1>
- <punto 2>
- <punto 3>
- <punto 4>

CAPITULOS:
<elige 5-8 cortes de la LISTA DE MARCAS de abajo, formato "m:ss Título corto". La primera marca debe ser 0:00. Usa solo marcas de la lista.>

FUENTES:
<las fuentes reales citadas en el guion/investigación, una por línea>

HASHTAGS: <#tag1 #tag2 #tag3 — máximo 3>
TAGS: <12-15 etiquetas separadas por comas, primera = frase clave exacta>
COMENTARIO FIJADO: <una pregunta abierta que invite a responder, sin repetir el título>
POST COMUNIDAD: <2-3 líneas anunciando el video con la pregunta del tema>
SHORT SUGERIDO: <escena de la lista (Sxx) que mejor funciona sola en 30-45s y por qué>
PANTALLA FINAL: <texto y tipo de video a enlazar>

LISTA DE MARCAS (inicio de cada escena, no inventes otras):
{marks}

GUION (extracto):
{script}
"""


def _scene_marks(job):
    """Marcas de tiempo reales por escena desde los audios TTS."""
    vo = job / "vo.json"
    if not vo.exists():
        return "(sin audios todavía: capítulos aproximados por escena)"
    items = json.loads(vo.read_text(encoding="utf-8"))
    lines, t = [], 0.0
    for it in items:
        au = job / "audio" / f"{it['id'].lower()}.mp3"
        dur = _probe_duration(au) if au.exists() else 0.0
        m, s = divmod(int(t), 60)
        lines.append(f"{m}:{s:02d} {it['id'].upper()} — "
                     f"{it['text'][:60]}...")
        t += dur
    return "\n".join(lines)


def run_paquete(generate_fn, p, job):
    if not generate_fn:
        return (False, "Necesita un backend LLM: configura una key en "
                       "Configuración o usa Ollama local.", [], None)
    sp = find_script(p)
    script = ""
    if sp:
        script = Path(sp).read_text(encoding="utf-8", errors="replace")[:6000]
    inv = job / "INVESTIGACION.md"
    if inv.exists():
        script += "\n\nINVESTIGACIÓN:\n" + inv.read_text(
            encoding="utf-8", errors="replace")[:3000]
    try:
        text, model = generate_fn(
            PAQUETE_PROMPT.format(title=p["title"], script=script,
                                  marks=_scene_marks(job)),
            system="Eres un editor de YouTube preciso y directo.")
    except Exception as e:
        return False, f"Error del modelo: {e}", [], None
    out = job / "PAQUETE.md"
    out.write_text(text, encoding="utf-8")
    return True, f"Paquete generado con {model} en {out}.", [str(out)], None


# ---------- TTS multi-motor (automático) ----------
def run_tts(job_dir, voice="edge:es-MX-DaliaNeural", language="es"):
    """Lee jobs/<slug>/vo.json ([{id, text}]) y genera audio/<id>.mp3.

    La voz es un spec "<motor>:<voz>" (ver tts_engine.py): edge neural
    (default, la más humana), kokoro local, piper local o hatch legacy.
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
    return tts_engine.speak_batch(items, voice, job / "audio", language)


# ---------- vo.json automático (desde storyboard o guion) ----------
_SENT_SPLIT = re.compile(r"(?<=[.!?…])\s+")


def build_vo_json(p, job):
    """Crea vo.json ([{id, text}]) desde STORYBOARD.md; si no hay, del guion.

    Devuelve (n_items, origen) o (0, "") si no hay material.
    """
    items = []
    sb = job / "STORYBOARD.md"
    if sb.exists():
        text = sb.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"###\s*(S\d+)(.*?)(?=###\s*S\d+|\Z)", text, re.S):
            vm = re.search(r"VOZ:\s*(.+)", m.group(2))
            if vm and vm.group(1).strip():
                items.append({"id": m.group(1).lower(),
                              "text": vm.group(1).strip()})
    if not items:
        sp = find_script(p)
        if sp:
            raw = Path(sp).read_text(encoding="utf-8", errors="replace")
            raw = re.sub(r"^#.*$", "", raw, flags=re.M)
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
        (job / "vo.json").write_text(
            json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
        return len(items), ("storyboard" if sb.exists() else "guion")
    return 0, ""


def run_tts_stage(p, job):
    extra = ""
    if not (job / "vo.json").exists():
        n, origen = build_vo_json(p, job)
        if not n:
            return (False, "Sin vo.json ni storyboard/guion para crearlo. "
                           "Genera primero el storyboard (etapa 5).", [], None)
        extra = f"vo.json creado desde {origen} ({n} líneas). "
    ok, log = run_tts(job, p["voice"], p["language"])
    arts = [str(a) for a in (job / "audio").glob("*.mp3")] if ok else []
    return ok, extra + log, arts, None


# ---------- animación: LLM genera Manim + render con autorreparación ----------
RIG_API = """API del rig (zenn_rig.py, ya importado con *). USO OBLIGATORIO:
los monigotes y objetos se crean SOLO con estas funciones. PROHIBIDO
construir monigotes con Circle/Line sueltos o redefinir el rig.
- stick_idle(pos, height=2.2, color=INK) -> monigote quieto
- stick_walk(fig, target, run_time=2.0) / stick_run(fig, target, run_time=1.5)
- stick_point(fig, target) / stick_think(fig, texto) / stick_group(n, ...)
- expresion(fig, tipo) -> cara sobre la cabeza (añadir tras posicionar):
  tipos: "normal", "feliz", "preocupado", "sorpresa", "triste", "miedo", "dormido"
- title_card(texto, color) -> tarjeta de capítulo a pantalla completa
- callout(texto, color=ORANGE, font_size=96) / arrow(start, end) / red_accent(obj)
- split_screen(izq, der) / clock_montage(radius)
- Fondos: fondo(color) pantalla completa; estrellas(n); luna(pos, radio, bg)
- Props clásicos: sol(), calendario(pos), pagina_calendario(), reloj_pared(),
  pastel(pos), red_seguridad(), caja(etiqueta, pos), camino(), casa(pos),
  oficina(pos), digitos(pos)
- Props con color (v2): perro(pos, color, escala), gato(pos, color, escala),
  dino(pos, color, escala), fuego(pos, escala), lapida(texto, pos),
  curva(pos, ancho, alto) [gráfica con punto rojo], planeta(pos, radio, color),
  casco_vikingo(pos, escala), hueso(pos, escala), vela(pos, escala),
  moneda_dorada(texto, pos, radio)
- Colores: WHITE, INK, YELLOW, ORANGE, RED, TEAL. Fondo blanco por defecto;
  para noche/espacio: self.add(fondo(INK)) al inicio y monigotes color=WHITE.
- Manim estándar: Scene, Text, FadeIn, FadeOut, Create, Write, Transform,
  LEFT/RIGHT/UP/DOWN/ORIGIN, self.play(), self.wait()
PROHIBIDO: Tex/MathTex (no hay LaTeX), archivos, internet, otros módulos."""

SCENE_PROMPT = """Eres programador de animación Manim para un canal de divulgación estilo Zenn.
Escribe el archivo Python COMPLETO de UNA escena. Debe contener EXACTAMENTE:
from manim import *
from zenn_rig import *

class {cls}(Scene):
    def construct(self):
        ...

{rig}

Escena {sid}:
VOZ (narración; en pantalla solo callouts cortos): {voz}
VISUAL: {visual}
Duración objetivo: ~{secs} segundos (suma de run_time + waits).

Reglas de calidad visual:
- 2-4 elementos por escena (monigote + props), no un solo objeto flotando.
- Usa expresion() acorde a la emoción de la narración.
- Usa props CON COLOR y, si la escena es nocturna/espacial, fondo oscuro.
- Movimientos simples pero presentes: entradas (FadeIn/Create), caminar,
  señalar, transformaciones. Nada de pantalla estática todo el tiempo.
Devuelve SOLO el código, sin explicaciones ni ```."""

FIX_PROMPT = """Este código Manim falló al renderizar. Corrígelo y devuelve el archivo COMPLETO, solo código.

ERROR:
{error}

CÓDIGO:
{code}"""


def _probe_duration(path):
    import shutil
    if not shutil.which("ffprobe"):
        return 0.0
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def _strip_fences(text):
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-z]*\n", "", t)
        t = re.sub(r"\n```\s*$", "", t)
    return t.strip()


def _rig_source():
    for c in (HERE / "scripts" / "zenn_rig.py", BASE / "scripts" / "zenn_rig.py",
              BASE / "panel" / "scripts" / "zenn_rig.py"):
        if c.exists():
            return c
    return None


def _parse_storyboard(job):
    sb = job / "STORYBOARD.md"
    scenes = []
    if not sb.exists():
        return scenes
    text = sb.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"###\s*(S\d+)(.*?)(?=###\s*S\d+|\Z)", text, re.S):
        vm = re.search(r"VOZ:\s*(.+)", m.group(2))
        xm = re.search(r"VISUAL:\s*(.+)", m.group(2))
        scenes.append({"id": m.group(1).lower(),
                       "voz": vm.group(1).strip() if vm else "",
                       "visual": xm.group(1).strip() if xm else ""})
    return scenes


def run_animacion(generate_fn, p, job):
    if not generate_fn:
        return (False, "Necesita un backend LLM para generar el código de "
                       "escenas (Configuración).", [], None)
    chk = subprocess.run([sys.executable, "-c", "import manim"],
                         capture_output=True, text=True)
    if chk.returncode != 0:
        return (False, "Manim no está instalado en el entorno del panel. "
                       "Instálalo: pip install manim (ya viene en "
                       "requirements.txt; si usas INICIAR.bat, borra la "
                       "carpeta .venv y vuelve a correrlo).", [], None)
    rig = _rig_source()
    if not rig:
        return False, "No encuentro scripts/zenn_rig.py en el paquete.", [], None
    scenes = _parse_storyboard(job)
    if not scenes:
        return (False, "Sin escenas: genera primero el storyboard "
                       "(etapa 5) — de ahí salen VOZ y VISUAL por escena.",
                [], None)
    sdir = job / "scripts"
    sdir.mkdir(parents=True, exist_ok=True)
    (sdir / "zenn_rig.py").write_text(
        rig.read_text(encoding="utf-8"), encoding="utf-8")
    vdir = job / "video" / "scenes"
    vdir.mkdir(parents=True, exist_ok=True)
    media = job / "media"

    logs, arts, fallos = [], [], []
    for sc in scenes:
        sid, cls = sc["id"], sc["id"].upper()
        out = vdir / f"{sid}.mp4"
        if out.exists() and out.stat().st_size > 0:
            logs.append(f"{cls}: ya renderizada, se omite.")
            arts.append(str(out))
            continue
        adur = _probe_duration(job / "audio" / f"{sid}.mp3")
        secs = round(adur) if adur else max(4, len(sc["voz"].split()) // 3)
        code = None
        err = ""
        for intento in range(3):
            try:
                if intento == 0:
                    prompt = SCENE_PROMPT.format(
                        cls=cls, rig=RIG_API, sid=cls, voz=sc["voz"],
                        visual=sc["visual"] or sc["voz"][:80], secs=secs)
                    code, _ = generate_fn(
                        prompt, system="Eres programador experto en Manim. "
                                       "Devuelves solo código Python válido.")
                else:
                    fixed, _ = generate_fn(
                        FIX_PROMPT.format(error=err[-1500:], code=code),
                        system="Eres programador experto en Manim. "
                               "Devuelves solo código Python válido.")
                    code = fixed
            except Exception as e:
                err = str(e)
                break
            code = _strip_fences(code)
            # Validación anti-desvío: si el modelo ignora el rig o no
            # define la clase, no gastamos un render; cuenta como intento.
            if "zenn_rig" not in code or f"class {cls}" not in code:
                err = ("El código no usa el rig (falta 'from zenn_rig "
                       f"import *' o la clase {cls}). Usa SOLO el rig "
                       "para monigotes y props; no los construyas con "
                       "Circle/Line sueltos.")
                continue
            f = sdir / f"{sid}.py"
            f.write_text(code, encoding="utf-8")
            r = subprocess.run(
                [sys.executable, "-m", "manim", "render", "-qm",
                 "--media_dir", str(media), "-o", sid, f.name, cls],
                cwd=str(sdir), capture_output=True, text=True, timeout=600)
            if r.returncode == 0:
                # Con -o <sid> el archivo final se llama <sid>.mp4
                # (ojo: partial_movie_files/ también contiene mp4s).
                cands = [q for q in media.glob(f"videos/**/{sid}.mp4")
                         if "partial_movie_files" not in q.parts]
                cands.sort(key=lambda q: q.stat().st_mtime)
                if cands:
                    out.write_bytes(cands[-1].read_bytes())
                    logs.append(f"{cls}: render OK "
                                f"({_probe_duration(out):.1f}s).")
                    arts.append(str(out))
                    err = ""
                    break
                err = "manim terminó sin generar el mp4."
            else:
                err = (r.stdout or "")[-1200:] + (r.stderr or "")[-1200:]
        if err:
            fallos.append(cls)
            logs.append(f"{cls}: FALLO tras intentos: {err[-300:]}")
    ok = not fallos
    head = (f"Animación: {len(arts)}/{len(scenes)} escenas renderizadas."
            if ok else
            f"Animación parcial: {len(arts)}/{len(scenes)} escenas. "
            f"Fallaron: {', '.join(fallos)} (reintenta la etapa: las ya "
            "hechas se omiten).")
    return ok, head + "\n" + "\n".join(logs[-20:]), arts, None


# ---------- ensamblado: video + audio (audio manda) + SRT ----------
def _srt_time(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _wrap_card(txt, width=44):
    """Parte una tarjeta larga en 2 líneas equilibradas."""
    if len(txt) <= width:
        return txt
    words = txt.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= width or not cur:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return "\n".join(lines[:2])


def _build_srt(items, durations):
    """SRT a nivel de frase: reparte la duración por caracteres."""
    cards, t = [], 0.0
    for it, dur in zip(items, durations):
        sents = [s.strip() for s in _SENT_SPLIT.split(it["text"]) if s.strip()]
        if not sents:
            sents = [it["text"]]
        total = sum(len(s) for s in sents) or 1
        cur = t
        for s in sents:
            d = dur * len(s) / total
            cards.append((cur, cur + d, _wrap_card(s)))
            cur += d
        t += dur
    out = []
    for i, (a, b, txt) in enumerate(cards, 1):
        out.append(f"{i}\n{_srt_time(a)} --> {_srt_time(b)}\n{txt}\n")
    return "\n".join(out)


def run_ensamblado(p, job):
    import shutil
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        return (False, "Falta ffmpeg/ffprobe en el PATH: instálalo para "
                       "poder ensamblar.", [], None)
    vdir = job / "video" / "scenes"
    scenes = sorted(vdir.glob("*.mp4")) if vdir.exists() else []
    if not scenes:
        return (False, "Sin videos de escenas: ejecuta antes la etapa 7 "
                       "(Animación).", [], None)
    vo_file = job / "vo.json"
    items = (json.loads(vo_file.read_text(encoding="utf-8"))
             if vo_file.exists() else [])
    texts = {it["id"].lower(): it["text"] for it in items}
    segdir = job / "video" / "segments"
    segdir.mkdir(parents=True, exist_ok=True)
    segs, srt_items, srt_durs, logs = [], [], [], []
    for sc in scenes:
        sid = sc.stem.lower()
        au = job / "audio" / f"{sid}.mp3"
        if not au.exists():
            return (False, f"Falta el audio de {sid.upper()} "
                           "(etapa 6 · TTS).", [], None)
        adur = _probe_duration(au)
        if adur <= 0:
            return False, f"No pude leer la duración de {au.name}.", [], None
        seg = segdir / f"{sid}.mp4"
        vf = (f"[0:v]tpad=stop_mode=clone:stop_duration=3600,"
              f"trim=duration={adur:.3f},setpts=PTS-STARTPTS,fps=30,"
              f"scale=1280:720,setsar=1[v]")
        r = subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", sc.name, "-i",
             f"../../audio/{sid}.mp3", "-filter_complex", vf,
             "-map", "[v]", "-map", "1:a", "-c:v", "libx264",
             "-preset", "medium", "-crf", "20", "-c:a", "aac",
             "-ar", "44100", f"../segments/{sid}.mp4"],
            cwd=str(vdir), capture_output=True, text=True, timeout=900)
        if r.returncode != 0:
            return False, f"ffmpeg falló en {sid}: {r.stderr[-400:]}", [], None
        segs.append(seg)
        srt_items.append({"id": sid, "text": texts.get(sid, "")})
        srt_durs.append(adur)
        logs.append(f"{sid.upper()}: {adur:.1f}s")
    vout = job / "video"
    listf = segdir / "list.txt"
    listf.write_text("".join(f"file '{s.name}'\n" for s in segs),
                     encoding="utf-8")
    final = vout / "final.mp4"
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", "list.txt", "-c", "copy", "../final.mp4"],
        cwd=str(segdir), capture_output=True, text=True, timeout=900)
    if r.returncode != 0:
        return False, f"ffmpeg falló al concatenar: {r.stderr[-400:]}", [], None
    srt = _build_srt(srt_items, srt_durs)
    srt_path = vout / "final.srt"
    srt_path.write_text(srt, encoding="utf-8")
    sub = vout / "final_con_subtitulos.mp4"
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", "final.mp4", "-vf",
         "subtitles='final.srt':force_style='FontName=Gochi Hand,"
         "FontSize=17,Outline=2,Shadow=0,MarginV=26,Alignment=2'",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-c:a", "copy", "final_con_subtitulos.mp4"],
        cwd=str(vout), capture_output=True, text=True, timeout=1800)
    arts = [str(final), str(srt_path)]
    if r.returncode == 0:
        arts.append(str(sub))
    total = sum(srt_durs)
    log = (f"Ensamblado OK: {len(segs)} escenas, {total:.0f}s totales "
           f"({total / 60:.1f} min).\n" + " · ".join(logs) +
           ("\nVersión con subtítulos quemados generada."
            if r.returncode == 0 else
            "\nAVISO: no se pudo quemar subtítulos (revisa final.srt)."))
    return True, log, arts, None


# ---------- miniaturas (automático) ----------
THUMB_PROPS = ["reloj", "calendario", "cerebro", "tierra", "cohete",
               "bombilla", "corazon", "libro", "moneda", "pregunta", "agujero",
               "perro", "dino", "dragon", "curva", "lapida", "luna"]

THUMB_CONCEPT_PROMPT = """Eres diseñador de miniaturas de YouTube para un canal de divulgación científica.
Video: "{title}"
Propón 3 variantes. Cada variante: un TEXTO de 3-5 palabras en MAYÚSCULAS
y un OBJETO de esta lista exacta: {props}.
REGLA CLAVE: el TEXTO debe contener SIEMPRE el sustantivo o fenómeno
principal del título (p. ej. si el video es de un hoyo negro, el texto
debe decir HOYO NEGRO). Nunca cortes la frase antes de esa palabra.
Responde EXACTAMENTE así, sin texto extra:
VARIANTE 1
TEXTO: <...>
OBJETO: <...>
VARIANTE 2
TEXTO: <...>
OBJETO: <...>
VARIANTE 3
TEXTO: <...>
OBJETO: <...>
"""

_KEYWORD_PROPS = [
    (("hoyo negro", "agujero negro", "agujero"), "agujero"),
    (("tiempo", "reloj", "edad", "envejec"), "reloj"),
    (("calendario", "año", "mes"), "calendario"),
    (("cerebro", "mente", "memoria", "pensar", "sueño", "soñar"), "cerebro"),
    (("tierra", "planeta", "clima", "océano", "mar", "volcán"), "tierra"),
    (("espacio", "luna", "marte", "estrella", "universo", "cohete"), "cohete"),
    (("idea", "luz", "invento", "descubr"), "bombilla"),
    (("salud", "corazón", "cuerpo", "dolor", "enfermedad"), "corazon"),
    (("historia", "libro", "antigu", "imperio", "guerra"), "libro"),
    (("dinero", "precio", "cuesta", "rico", "econom"), "moneda"),
]

_STOPWORDS = {"qué", "que", "cómo", "como", "por", "si", "pasaría", "pasaria",
              "en", "un", "una", "el", "la", "los", "las", "de", "del", "al",
              "a", "y", "o", "es", "son", "cuándo", "cuando", "dónde", "donde"}


def _short_text(title):
    """Texto corto SIN cortar el sustantivo clave: quita muletillas."""
    clean = re.sub(r"[¿?¡!]", " ", title).lower().strip()
    clean = re.sub(r"^(por qué|porque)\s+", "", clean)
    words = [w for w in clean.split() if w not in _STOPWORDS]
    if not words:
        words = clean.split()
    return " ".join(words[:5]).upper() or "EL PORQUÉ"


def _fallback_concept(title):
    t = title.lower()
    prop = "pregunta"
    for keys, name in _KEYWORD_PROPS:
        if any(k in t for k in keys):
            prop = name
            break
    return _short_text(title), prop


def thumbnail_concepts(generate_fn, title):
    """Devuelve 3 conceptos [{text, prop}]. LLM si hay; si no, heurística."""
    if generate_fn:
        try:
            text, _ = generate_fn(
                THUMB_CONCEPT_PROMPT.format(title=title,
                                            props=", ".join(THUMB_PROPS)),
                system="Eres diseñador de miniaturas de YouTube.")
            concepts = []
            for block in text.split("VARIANTE")[1:]:
                m_text = re.search(r"TEXTO:\s*(.+)", block)
                m_prop = re.search(r"OBJETO:\s*(\w+)", block)
                if m_text:
                    prop = (m_prop.group(1).lower() if m_prop else "pregunta")
                    if prop not in THUMB_PROPS:
                        prop = "pregunta"
                    concepts.append({"text": m_text.group(1).strip()[:60],
                                     "prop": prop})
            if len(concepts) >= 3:
                return concepts[:3]
        except Exception:
            pass
    text, prop = _fallback_concept(title)
    return [{"text": text, "prop": prop},
            {"text": text, "prop": "pregunta"},
            {"text": text, "prop": prop}]


def thumbs_dir():
    for c in (HERE / "thumbnails", BASE / "thumbnails",
              BASE / "panel" / "thumbnails"):
        if (c / "generate_thumbnails.py").exists():
            return c
    return HERE / "thumbnails"


def run_thumbnails(project_id=None, title="", generate_fn=None):
    """Genera miniaturas 1280x720 ilustradas en thumbnails/thumb_<id>_*.png."""
    here = Path(__file__).resolve().parent
    tdir = thumbs_dir()
    script = tdir / "generate_thumbnails.py"
    if not script.exists():
        return False, "No encuentro thumbnails/generate_thumbnails.py."
    if project_id:
        concepts = thumbnail_concepts(generate_fn, title)
        cfile = tdir / f"concepts_{project_id}.json"
        cfile.write_text(json.dumps(concepts, ensure_ascii=False),
                         encoding="utf-8")
    cmd = [sys.executable, str(script)]
    if project_id:
        cmd.append(str(project_id))
    return run(cmd, cwd=BASE, timeout=300)


def run_miniatura(generate_fn, p):
    pid = p["id"]
    ok, log = run_thumbnails(pid, p["title"], generate_fn)
    if not ok:
        return False, log, [], None
    arts = [str(a) for a in thumbs_dir().glob(f"thumb_{pid}_*.png")]
    return True, log, arts, None


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


# ---------- dispatcher de etapas ----------
_NO_LLM = ("Esta etapa necesita un modelo: elige un backend en el sidebar "
           "y pon su API key en Configuración (o usa Ollama local).")


def execute_stage(p, stage, generate_fn=None):
    """Devuelve (ok, log, artefactos, estado_sugerido|None)."""
    job = job_dir_of(p)
    kind = pget(p, "kind", "largo")
    try:
        if stage == "investigacion":
            return run_investigacion(generate_fn, p["title"], job)
        if stage == "guion":
            return run_guion_draft(generate_fn, p, job, kind)
        if stage == "verificacion":
            sp = find_script(p)
            if not sp:
                return False, "Sin guion para verificar.", [], None
            dois, pmids = extract_references(
                Path(sp).read_text(encoding="utf-8"))
            log = (f"DOIs: {len(dois)}, PMIDs: {len(pmids)}\n" +
                   "\n".join(dois + [f"PMID:{x}" for x in pmids]))
            return True, log, [], None
        if stage == "storyboard":
            return run_storyboard(generate_fn, p, job)
        if stage == "tts":
            return run_tts_stage(p, job)
        if stage == "animacion":
            return run_animacion(generate_fn, p, job)
        if stage == "ensamblado":
            return run_ensamblado(p, job)
        if stage == "miniatura":
            return run_miniatura(generate_fn, p)
        if stage == "paquete":
            return run_paquete(generate_fn, p, job)
        if stage in MANUAL_STAGES:
            return (False,
                    f"Etapa manual: {STAGE_HINTS.get(stage, '')} "
                    "Al terminarla, pulsa 'Marcar hecho'.",
                    [], "pendiente")
        return False, (f"Etapa '{stage}' sin ejecutor. "
                       "Usa 'Marcar hecho' cuando la completes."), [], None
    except Exception as e:
        return False, f"Error: {e}", [], None


def run_all(conn, p, generate_fn, on_step=None):
    """Ejecuta las etapas EN ORDEN y se detiene donde hace falta un humano.

    on_step(stage, ok, log) se llama tras cada etapa ejecutada.
    Devuelve (motivo, detalle):
      ("done", "")        todo completado
      ("gate", gate)      esperando aprobación humana (guion/miniatura/tema)
      ("manual", stage)   etapa manual pendiente (animacion/ensamblado/...)
      ("error", stage)    una etapa falló; ver su log
    """
    import db as _db
    pid = p["id"]
    for s in _db.list_stages(conn, pid):
        name, stt = s["stage"], s["status"]
        if stt in ("ok", "manual", "omitido"):
            continue
        if name == "tema":
            if _db.get_approval(conn, pid, "tema")["status"] == "aprobado":
                _db.set_stage(conn, pid, name, "ok",
                              "Tema aprobado en la bandeja.")
                if on_step:
                    on_step(name, True, "Tema aprobado.")
                continue
            return "gate", "tema"
        if name == "guion":
            if _db.get_approval(conn, pid, "guion")["status"] == "aprobado":
                continue
            if stt != "en-curso":
                ok, log, arts, sugg = execute_stage(p, name, generate_fn)
                _db.set_stage(conn, pid, name,
                              sugg or ("ok" if ok else "fallo"), log, arts)
                if on_step:
                    on_step(name, ok, log)
                if not ok:
                    return "error", name
            return "gate", "guion"
        # El resto depende del guion aprobado.
        if name in ("verificacion", "storyboard", "tts", "ensamblado"):
            if _db.get_approval(conn, pid, "guion")["status"] != "aprobado":
                return "gate", "guion"
        if name in MANUAL_STAGES:
            return "manual", name
        if name == "paquete":
            if pget(p, "kind", "largo") == "largo" and \
               _db.get_approval(conn, pid, "miniatura")["status"] != "aprobado":
                return "gate", "miniatura"
        ok, log, arts, sugg = execute_stage(p, name, generate_fn)
        _db.set_stage(conn, pid, name,
                      sugg or ("ok" if ok else "fallo"), log, arts)
        if on_step:
            on_step(name, ok, log)
        if not ok:
            return "error", name
    return "done", ""


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
