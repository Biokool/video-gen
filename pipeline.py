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
import time
import ast
from pathlib import Path

HERE = Path(__file__).resolve().parent

PANEL_VERSION = "v15"  # se muestra en el pie del sidebar; subir en cada release
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
                 "escena falla, intenta repararla solo (máx 2 intentos). Si "
                 "se agota la cuota del backend, la etapa se DETIENE sola "
                 "(no sigue fallando en cascada): reanuda después, las "
                 "hechas se omiten. Cada ejecución deja su log completo en "
                 "jobs/<id>/logs/.",
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
4. APERTURA: ¿tiene el saludo fijo del canal + hook en los primeros 20 segundos? (1 línea)
5. RETENCIÓN: ¿hay 3-4 picos de información marcados? ¿cada bloque termina en open loop? (sí/no + dónde faltan)
6. CIERRE: ¿tiene la despedida fija del canal? (sí/no)
7. ORTOGRAFÍA: lista palabras con tildes mal puestas o caracteres raros (è, ò, à, ù no existen en español).
8. Fallos concretos a corregir (lista corta, sin rodeos).

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
STORYBOARD_PROMPT = """Eres director de animación de un canal de divulgación con dibujos
minimalistas de colores vivos (estilo Zenn / Memorias de Pez).
Divide este guion en escenas numeradas. Por escena: el texto de narración LITERAL
y una descripción visual de 1 línea (qué personaje u objeto se ve, con qué
expresión y colores).

REGLAS:
- RITMO POR DEFECTO: escenas CORTAS de 8-12 segundos (~25-35 palabras de VOZ
  por escena). Más cortes = más dinamismo = más retención. Parte el guion en
  TANTAS escenas como necesites (un video de 10 minutos → 50-60 escenas).
  PROHIBIDO meter 3 o más frases en una sola escena si puedes partirla en dos.
- PROTAGONISTA EN TODAS: el personaje principal (protagonista) aparece en
  cada escena como conductor. Varía su playera por bloque temático
  (naranja=intro, azul=presentación, verde=transmisión, roja=curiosidad,
  amarilla=pregunta, rosa=detalles, teal=cierre) y su expresión según la
  emoción de la narración.
- La PRIMERA escena es la bienvenida: tarjeta_canal() + el saludo del guion.
- La ÚLTIMA escena es la despedida del guion (tono cálido, cierre del canal).
- Cada escena: 2-4 elementos, nada encimado, nada cortado por los bordes,
  nada de texto en la franja inferior (ahí van los subtítulos).

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
    # Anti-truncado ESTRUCTURAL: si el storyboard no cubre el guion, la etapa
    # FALLA (no avisa y sigue). Un storyboard cortado = video cortado.
    voz_words = sum(len(m.group(1).split())
                    for m in re.finditer(r"VOZ:\s*(.+)", text))
    guion_words = len(re.sub(r"^#.*$", "", script, flags=re.M).split())
    if guion_words > 0 and voz_words < 0.7 * guion_words:
        return False, (
            f"⛔ STORYBOARD TRUNCADO: cubre ~{voz_words} palabras de "
            f"{guion_words} del guion (mínimo 70%). Si continuara, el video "
            f"saldría cortado (como el proyecto 18: 3 min en vez de 9). "
            f"Opciones: 1) pulsa «↪️ Continuar storyboard» aquí abajo para "
            f"que el modelo complete las escenas faltantes desde "
            f"S{n + 1:02d} sin regenerar desde cero; 2) reintenta la etapa "
            f"con otro backend."), [str(out)], None
    return True, (f"Storyboard con {model}: {n} escenas en {out} "
                  f"(~{voz_words} palabras de VOZ)."), [str(out)], None


def run_continuar_storyboard(generate_fn, p, job):
    """Continúa un storyboard truncado desde la última escena existente.

    No regenera desde cero: pide al modelo solo las escenas faltantes
    (las partes del guion aún sin cubrir) y las agrega a STORYBOARD.md.
    Devuelve (ok, log, artefactos, None).
    """
    if not generate_fn:
        return (False, "Necesita un backend LLM.", [], None)
    sb = job / "STORYBOARD.md"
    if not sb.exists():
        return False, "No hay STORYBOARD.md: corre la etapa storyboard.", [], None
    text = sb.read_text(encoding="utf-8", errors="replace")
    nums = [int(m.group(1)) for m in re.finditer(r"### S(\d+)", text)]
    if not nums:
        return False, "El storyboard no tiene escenas ### Sxx.", [], None
    n = max(nums)
    sp = find_script(p)
    script = Path(sp).read_text(encoding="utf-8", errors="replace") if sp else ""
    prompt = (
        f"Este storyboard quedó TRUNCADO en S{n:02d}. Continúa desde "
        f"S{n + 1:02d} cubriendo ÚNICAMENTE las partes del guion que aún no "
        f"tienen escena, hasta la despedida final del guion (tono cálido, "
        f"cierre del canal). Mismo formato exacto por escena:\n"
        f"### SXX\nVOZ: <texto literal del guion>\nVISUAL: <descripción>\n\n"
        f"REGLAS: escenas de 8-12s (~25-35 palabras de VOZ); PROTAGONISTA en "
        f"todas; NO repitas escenas ya existentes.\n\n"
        f"STORYBOARD EXISTENTE (referencia, no lo repitas):\n{text[-6000:]}\n\n"
        f"GUION COMPLETO:\n{script[:12000]}")
    try:
        new_text, model = generate_fn(
            prompt, system="Eres director de animación minimalista.")
    except Exception as e:
        return False, f"Error del modelo: {e}", [], None
    # Quédate solo con bloques nuevos (número > n)
    partes = re.split(r"(?m)^(?=### S\d+)", new_text)
    nuevos = []
    for bl in partes:
        m = re.match(r"### S(\d+)", bl.strip())
        if m and int(m.group(1)) > n:
            nuevos.append(bl.strip())
    if not nuevos:
        return False, ("El modelo no devolvió escenas nuevas (S{n + 1:02d}+). "
                       "Reintenta con otro backend."), [str(sb)], None
    with open(sb, "a", encoding="utf-8") as f:
        f.write("\n\n" + "\n\n".join(nuevos) + "\n")
    total = n + len(nuevos)
    # Revalida cobertura
    full = sb.read_text(encoding="utf-8", errors="replace")
    voz_words = sum(len(m.group(1).split())
                    for m in re.finditer(r"VOZ:\s*(.+)", full))
    guion_words = len(re.sub(r"^#.*$", "", script, flags=re.M).split())
    if guion_words > 0 and voz_words < 0.7 * guion_words:
        return False, (
            f"Se agregaron {len(nuevos)} escenas (total S{total:02d}) pero la "
            f"cobertura sigue baja (~{voz_words}/{guion_words} palabras). "
            f"Pulsa «↪️ Continuar storyboard» otra vez."), [str(sb)], None
    return True, (f"Storyboard completado con {model}: {len(nuevos)} escenas "
                  f"nuevas, total {total} (S01–S{total:02d})."), [str(sb)], None


# ---------- paquete de publicación (asistida) ----------
PAQUETE_PROMPT = """Eres el editor de un canal de YouTube de divulgación científica en español (estilo Zenn).
Genera el paquete de publicación COMPLETO para el video "{title}", con EXACTAMENTE este formato.

REGLAS DE FORMATO (obligatorias: romperlas daña la credibilidad del canal):
- PROHIBIDO markdown: nada de **, ##, ### ni *cursivas*. YouTube lo muestra como texto crudo y se ve como error de automatización.
- Los encabezados dentro de las secciones son texto plano con emoji, p. ej. "🔍 LO QUE VERÁS:".
- Viñetas con "•", nunca con guiones.

TITULOS (máx 60 caracteres cada uno, INCLUYENDO el sufijo):
1. <opción 1: fórmula pregunta directa, afirmación fuerte, número o superlativo + palabra clave al frente. Gancho honesto, sin clickbait falso. Ej: "¿Por qué los mosquitos siempre te pican a TI?">
2. <opción 2>
3. <opción 3>
A las 3 opciones agrégales al final " | En {dur_min} minutos" (promesa de duración, fórmula de Memorias de Pez; el total con sufijo no pasa de 60 caracteres: acorta el título base si hace falta).

DESCRIPCION:
<líneas 1-2: el gancho en segunda persona — la pregunta del video + qué se lleva el espectador. Es lo que se ve sin desplegar: lo más importante de todo>
<1 línea de valor: qué aprenderá, con la palabra clave>

LO QUE VERAS:
<4-6 líneas, cada una empezando con "•", puntos concretos del video>

CAPITULOS:
<elige 5-8 cortes de la LISTA DE MARCAS de abajo, formato "m:ss Título corto". La primera marca debe ser 0:00. Usa solo marcas de la lista.>

FUENTES:
<las fuentes reales citadas en el guion/investigación, una por línea, formato "Autor (año). Título.">

CTA:
<1 línea invitando a suscribirse, p. ej: "🔔 Suscríbete a El Porqué para resolver el siguiente porqué cada semana.">

PREGUNTA:
<1 pregunta abierta para los comentarios, sin repetir el título, terminada en "👇">

HASHTAGS: <#tag1 #tag2 #tag3 — de 3 a 5, el primero = la palabra clave principal en minúsculas>
TAGS: <12-15 etiquetas separadas por comas, en minúsculas, ESPECÍFICAS (nada de "mundo", "ciencia" solos), la primera = la frase clave exacta>
COMENTARIO FIJADO: <pregunta abierta distinta a la de PREGUNTA, que invite a responder>
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
    # Duración real del video (para el sufijo "| En N minutos" de los
    # títulos, fórmula de Memorias de Pez): final.mp4 si existe, si no
    # suma de los audios TTS.
    dur_min = 10
    final = job / "video" / "final_con_subtitulos.mp4"
    if not final.exists():
        final = job / "video" / "final.mp4"
    if final.exists():
        d = _probe_duration(final)
        if d:
            dur_min = max(1, int(round(d / 60)))
    else:
        t = 0.0
        try:
            for it in json.loads((job / "vo.json").read_text(
                    encoding="utf-8")):
                au = job / "audio" / f"{it['id'].lower()}.mp3"
                if au.exists():
                    t += _probe_duration(au) or 0.0
        except Exception:
            pass
        if t > 60:
            dur_min = max(1, int(round(t / 60)))
    try:
        text, model = generate_fn(
            PAQUETE_PROMPT.format(title=p["title"], script=script,
                                  marks=_scene_marks(job),
                                  dur_min=dur_min),
            system="Eres un editor de YouTube preciso y directo.")
    except Exception as e:
        return False, f"Error del modelo: {e}", [], None
    out = job / "PAQUETE.md"
    out.write_text(text, encoding="utf-8")
    return True, f"Paquete generado con {model} en {out}.", [str(out)], None


# ---------- TTS multi-motor (automático) ----------
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
_SENT_SPLIT = re.compile(r"(?<=[.!?…])\s+")


# ---------- progreso con ETA (lo pinta la app) ----------
def fmt_eta(secs):
    if secs is None:
        return ""
    secs = int(round(secs))
    if secs < 60:
        return f"~{secs}s restantes"
    m, s = divmod(secs, 60)
    return f"~{m}m{s:02d}s restantes" if m < 60 else f"~{m // 60}h{(m % 60):02d}m restantes"


class Progreso:
    """Reporta avance de una etapa larga con ETA.

    callback(stage_key, done, total, detalle): la app lo usa para
    pintar barra de progreso. `detalle` ya trae el ETA calculado
    con la media de lo que tardó cada elemento hasta ahora.
    """
    def __init__(self, stage, callback=None):
        self.stage = stage
        self.cb = callback
        self.t0 = None
        self.durs = []

    def start(self, total, label=""):
        self.t0 = time.time()
        self.durs = []
        self._emit(0, total, label or "iniciando…", None)

    def item(self, done, total, label=""):
        if self.t0 is not None and done > 0:
            self.durs.append(time.time() - self.t0 - sum(self.durs))
        eta = None
        if self.durs:
            eta = (sum(self.durs) / len(self.durs)) * (total - done)
        self._emit(done, total, label, eta)

    def _emit(self, done, total, label, eta):
        if not self.cb:
            return
        det = f"{label} · {done}/{total}" if label else f"{done}/{total}"
        if eta:
            det += f" · {fmt_eta(eta)}"
        try:
            self.cb(self.stage, done, total, det)
        except Exception:
            pass


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


def run_tts_stage(p, job, progress=None):
    extra = ""
    if not (job / "vo.json").exists():
        n, origen = build_vo_json(p, job)
        if not n:
            return (False, "Sin vo.json ni storyboard/guion para crearlo. "
                           "Genera primero el storyboard (etapa 5).", [], None)
        extra = f"vo.json creado desde {origen} ({n} líneas). "
    ok, log = run_tts(job, p["voice"], p["language"], progress=progress)
    arts = [str(a) for a in (job / "audio").glob("*.mp3")] if ok else []
    full = extra + log
    logf = _guardar_log(job, "tts", [full])
    if logf:
        full += f"\n📄 Log completo de esta ejecución: {logf}"
    return ok, full, arts, None


# ---------- animación: LLM genera Manim + render con autorreparación ----------
RIG_API = """API del rig (zenn_rig.py, ya importado con *). USO OBLIGATORIO:
los personajes y objetos se crean SOLO con estas funciones. PROHIBIDO
construir personajes con Circle/Line sueltos o redefinir el rig.

PERSONAJE PRINCIPAL — "EL PORQUÉ" (protagonista en TODAS las escenas):
  protagonista(pos, playera, altura=3.0, expresion, pose) -> el conductor:
  cabezón de ojos grandes, playera de color, extremidades negras simples.
  LAYOUT: con banda_titulo()/titulo_seguro() arriba, el protagonista va
  ABAJO (pos con y<=-1.2, altura<=2.6; p. ej. pos=DOWN*1.2+LEFT*3.5);
  sin banda puede ir al centro (pos=ORIGIN, altura=3.0).
  playera: "naranja" (default/intro), "azul", "verde", "roja", "amarilla",
    "rosa", "teal", "morada", "negra", "blanca" (strings en español;
    también valen las constantes PLAYERA_NARANJA/AZUL/...).
    Cambia el color por bloque temático.
  expresion: feliz, alegria_pura, triste, enojado, sorpresa,
    mente_explotada, pensando, confundido, miedo, decidido, euforico,
    cansado, dormido, nervioso, sarcastico.
  pose: de_pie, senalando, brazos_cruzados, caminando, corriendo.
  cambiar_cara(prota, tipo) -> cambia la expresión en el acto (para animar).
  version_prota(n, pos) -> atajo: 1=intro naranja, 2=presentación azul,
    4=curiosidad roja, 5=pregunta amarilla, 6=transmisión verde señalando,
    7=detalles rosa, 8=final teal.
- Monigote clásico (secundario): stick_idle(pos, height=2.2, color=INK),
  stick_walk(fig, target, run_time=2.0), stick_run(fig, target, run_time=1.5),
  stick_point(fig, target), stick_think(fig, texto), stick_group(n, ...),
  expresion(fig, tipo): "normal", "feliz", "preocupado", "sorpresa",
  "triste", "miedo", "dormido"
- title_card(texto, color) -> tarjeta de capítulo a pantalla completa
- callout(texto, color, pos) -> dato destacado COMPACTO (se auto-ajusta;
  nunca sale del encuadre aunque pidas pos lejana: el rig lo recorta).
  pos p. ej. pos=RIGHT*3.4+UP*1, SIEMPRE al lado contrario del
  protagonista, NUNCA encima. PROHIBIDO font_size>72 (gigante = rechazo).
  / arrow(start, end) / red_accent(obj)
- split_screen(izq, der) / clock_montage(radius)
- Fondos: fondo(color) pantalla completa; estrellas(n); luna(pos, radio, bg)
- Props clásicos: sol(), calendario(pos), pagina_calendario(), reloj_pared(),
  pastel(pos), red_seguridad(), caja(etiqueta, pos), camino(), casa(pos),
  oficina(pos), digitos(pos), adn(pos, escala), grafica_barras(pos, valores,
  ancho, etiquetas), lupa(pos, escala), fondo_papel() [fondo crema cálido
  opcional: self.add(fondo_papel()) al inicio]
- Props con color (v2): perro(pos, color, escala), gato(pos, color, escala),
  dino(pos, color, escala), fuego(pos, escala), lapida(texto, pos),
  curva(pos, ancho, alto) [gráfica con punto rojo], planeta(pos, radio, color),
  casco_vikingo(pos, escala), hueso(pos, escala), vela(pos, escala),
  moneda_dorada(texto, pos, radio)
- Texto SEGURO (v3, auto-ajustado: nunca se sale del encuadre):
  banda_titulo(texto, color) -> banda superior con texto que se encoge solo;
  titulo_seguro(texto, color) -> título auto-escalado;
  etiqueta(texto, (x, y)) -> etiqueta pequeña (nunca baja a subtítulos);
  tarjeta_canal() -> tarjeta de apertura/cierre "EL PORQUÉ"
- Personajes ilustrados (v3): personaje(pos, cuerpo, altura, expresion_tipo)
  [cuerpo de color + cara: normal/feliz/preocupado/sorpresa/triste/miedo],
  pez(pos, color, escala), matraz(pos, escala, liquido), ojo_grande(pos, escala)
- Paleta: MOSTAZA, CORAL, AZUL_MARINO, CREMA, además de WHITE, INK, YELLOW,
  ORANGE, RED, TEAL. Fondo blanco por defecto; para noche/espacio:
  self.add(fondo(INK)) al inicio y monigotes color=WHITE.
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
- Código COMPACTO (~40-70 líneas): nada de comentarios largos.

COMPOSICIÓN — OBLIGATORIO (la cámara mide 14.22 x 8: x de -7.1 a 7.1,
y de -4 a 4):
- ZONA DE SUBTÍTULOS: entre y=-2.4 y y=-4 van los subtítulos quemados.
  NUNCA pongas texto, títulos, bandas ni elementos importantes ahí.
- Títulos y bandas: usa SIEMPRE banda_titulo() o titulo_seguro()
  (se auto-ajustan; PROHIBIDO Text() gigante manual que se salga).
- UNA SOLA banda/título/callout por escena: PROHIBIDO llamar más de una
  vez en la misma escena a banda_titulo(), titulo_seguro(), title_card(),
  tarjeta_canal() o callout() (se enciman y tapan todo). Si la escena
  necesita dos ideas, usa split_screen() o etiquetas pequeñas.
- LAYOUT CON BANDA (obligatorio): si la escena lleva banda_titulo() o
  titulo_seguro() ARRIBA, el protagonista va ABAJO: pos con y<=-1.2 y
  altura<=2.6 (p. ej. pos=DOWN*1.2+LEFT*3.5 o pos=DOWN*1.2+RIGHT*3.5).
  La cabeza del protagonista NUNCA entra a la zona y>1.7: la banda la
  taparía (es el fallo más repetido en producción y se rechaza por
  validación).
- Sin banda: el protagonista puede ir al centro (pos=ORIGIN, altura=3.0).
- PROHIBIDO Text() con font_size mayor a 60: para títulos usa
  banda_titulo()/titulo_seguro(); para datos destacados, callout();
  para etiquetas, etiqueta(). El texto crudo grande se corta en los
  bordes (también se rechaza por validación).
- Etiquetas: usa etiqueta(texto, (x, y)) con y >= -1.9.
- callout(): dato compacto con pos= (p. ej. pos=RIGHT*3.4+UP*1), al lado
  CONTRARIO del protagonista; NUNCA encima de él. El rig impide que salga
  del encuadre, pero el validador RECHAZA el solape con el protagonista:
  si el prota va a la izquierda, el callout va a la derecha y viceversa.
- SEPARACIÓN: un elemento grande por zona (izquierda/derecha,
  arriba/abajo); deja >=1.5 unidades entre elementos; NADA puede tapar
  a otro: ni bocadillos sobre texto, ni figuras sobre etiquetas,
  ni círculos/flechas sobre subtítulos.
- Todo el texto en pantalla entre y=-2.2 y y=3.4.
Devuelve SOLO el código, sin explicaciones ni ```."""

FIX_PROMPT = """Este código Manim falló al renderizar. Corrígelo y devuelve el archivo COMPLETO, solo código.
Respeta al carácter las firmas REALES del rig: si un parámetro no aparece ahí, no existe (inventarlo vuelve a fallar).

{rig}

ERROR:
{error}

CÓDIGO:
{code}"""


def _rig_api_text(rig_file=None):
    """RIG_API + firmas reales del rig, para que el modelo no invente kwargs."""
    sigs = []
    try:
        p = Path(rig_file) if rig_file else None
        if p and p.exists():
            import ast
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                        and not node.name.startswith("_"):
                    try:
                        sigs.append(f"{node.name}({ast.unparse(node.args)})")
                    except Exception:
                        pass
    except Exception:
        sigs = []
    if not sigs:
        return RIG_API
    bloque = ("Firmas REALES del rig (respétalas; NO inventes parámetros):\n"
              + "\n".join("- " + s for s in sigs) + "\n\n")
    return bloque + RIG_API


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


def _guardar_log(job, stage, lineas):
    """Guarda el log COMPLETO de una ejecución en jobs/<id>/logs/.

    El panel solo muestra la cola en la BD; este archivo conserva cada
    línea (qué escena se hizo, cuál se omitió, cuál falló y por qué)
    para revisar cualquier corrida después.
    Devuelve la ruta del archivo o "".
    """
    try:
        d = Path(job) / "logs"
        d.mkdir(parents=True, exist_ok=True)
        fp = d / f"{stage}_{time.strftime('%Y%m%d_%H%M%S')}.log"
        fp.write_text("\n".join(lineas), encoding="utf-8")
        return str(fp)
    except Exception:
        return ""


def _strip_fences(text):
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-z]*\n", "", t)
        t = re.sub(r"\n```\s*$", "", t)
    return t.strip()


# --- evaluador restringido de coordenadas Manim (para el chequeo de layout) ---
_MANIM_VEC = {
    "ORIGIN": (0.0, 0.0, 0.0),
    "LEFT": (-1.0, 0.0, 0.0), "RIGHT": (1.0, 0.0, 0.0),
    "UP": (0.0, 1.0, 0.0), "DOWN": (0.0, -1.0, 0.0),
}


def _eval_vec(node):
    """Evalúa expresiones simples de coordenadas Manim.

    Devuelve ("vec", (x, y)) o ("num", v) o None si no se puede resolver.
    Soporta: ORIGIN/LEFT/RIGHT/UP/DOWN, números, tuplas, np.array([...]),
    +, -, *, y negación. Cualquier otra cosa → None (no se puede probar).
    """
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return ("num", float(node.value))
        return None
    if isinstance(node, ast.Name):
        v = _MANIM_VEC.get(node.id)
        return ("vec", (v[0], v[1])) if v else None
    if isinstance(node, (ast.Tuple, ast.List)) and len(node.elts) >= 2:
        x, y = _eval_vec(node.elts[0]), _eval_vec(node.elts[1])
        if x and x[0] == "num" and y and y[0] == "num":
            return ("vec", (x[1], y[1]))
        return None
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        v = _eval_vec(node.operand)
        if v and v[0] == "vec":
            return ("vec", (-v[1][0], -v[1][1]))
        if v and v[0] == "num":
            return ("num", -v[1])
        return None
    if isinstance(node, ast.BinOp):
        l, r = _eval_vec(node.left), _eval_vec(node.right)
        if not l or not r:
            return None
        if isinstance(node.op, ast.Add) and l[0] == "vec" and r[0] == "vec":
            return ("vec", (l[1][0] + r[1][0], l[1][1] + r[1][1]))
        if isinstance(node.op, ast.Sub) and l[0] == "vec" and r[0] == "vec":
            return ("vec", (l[1][0] - r[1][0], l[1][1] - r[1][1]))
        if isinstance(node.op, ast.Mult):
            if l[0] == "vec" and r[0] == "num":
                return ("vec", (l[1][0] * r[1], l[1][1] * r[1]))
            if l[0] == "num" and r[0] == "vec":
                return ("vec", (l[1] * r[1][0], l[1] * r[1][1]))
        return None
    if isinstance(node, ast.Call):
        f = node.func
        if (isinstance(f, ast.Attribute) and f.attr == "array"
                and isinstance(f.value, ast.Name) and f.value.id == "np"
                and node.args):
            return _eval_vec(node.args[0])
        return None
    return None


def _kw(call, nombre, posicional=None, default=None):
    for kw in call.keywords:
        if kw.arg == nombre:
            return kw.value
    if posicional is not None and len(call.args) > posicional:
        return call.args[posicional]
    return default


def _num(node, default):
    v = _eval_vec(node)
    if v and v[0] == "num":
        return v[1]
    return default


# Helpers de texto cuyo posicionamiento se valida contra el protagonista.
_TEXTO_POS = {"callout", "etiqueta"}
# Tamaños por defecto del rig (scripts/zenn_rig.py)
_TXT_DEF = {"callout": {"font_size": 60, "ancho_max": 7.0, "pad": 0.7},
            "etiqueta": {"font_size": 40, "ancho_max": 5.5, "pad": 0.0}}


def _nombre_llamada(node):
    f = node.func
    if isinstance(f, ast.Attribute):
        return f.attr
    if isinstance(f, ast.Name):
        return f.id
    return ""


def _texto_de(call, helper):
    """Texto del helper (arg 0 o kwarg text/texto)."""
    if call.args:
        try:
            return str(ast.literal_eval(call.args[0]))
        except Exception:
            return ""
    for kw in call.keywords:
        if kw.arg in ("text", "texto"):
            try:
                return str(ast.literal_eval(kw.value))
            except Exception:
                return ""
    return ""


def _cajas_texto(tree):
    """Cajas de callout()/etiqueta(): (centro, w, h) finales.

    Sigue .move_to()/.shift() encadenados (`x = callout(...).move_to(E)`)
    o en sentencias separadas (`x.move_to(E)`). Si la posición no es
    evaluable, se omite (el rig la encuadra en runtime de todos modos).
    """
    nodos = sorted(ast.walk(tree),
                   key=lambda n: (getattr(n, "lineno", 0),
                                  getattr(n, "col_offset", 0)))
    # var -> [helper, call, [(mov, expr)]] en orden de aparición
    vars_txt = {}
    for node in nodos:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            v, moves = node.value, []
            while isinstance(v, ast.Call) and isinstance(v.func, ast.Attribute) \
                    and v.func.attr in ("move_to", "shift"):
                moves.append((v.func.attr,
                              v.args[0] if v.args else None))
                v = v.func.value
            if isinstance(v, ast.Call) and _nombre_llamada(v) in _TEXTO_POS:
                vars_txt[node.targets[0].id] = [_nombre_llamada(v), v,
                                                list(reversed(moves))]
    for node in nodos:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            c, f = node.value, node.value.func
            if isinstance(f, ast.Attribute) and f.attr in ("move_to", "shift") \
                    and isinstance(f.value, ast.Name) \
                    and f.value.id in vars_txt:
                vars_txt[f.value.id][2].append(
                    (f.attr, c.args[0] if c.args else None))
    cajas = []
    for var, (helper, call, moves) in vars_txt.items():
        d = _TXT_DEF[helper]
        fs = _num(_kw(call, "font_size", default=None), d["font_size"])
        am = _num(_kw(call, "ancho_max", default=None), d["ancho_max"])
        texto = _texto_de(call, helper)
        # centro base: kwarg pos= (callout) o arg 1 pos (etiqueta)
        base = _kw(call, "pos", default=None)
        if base is None and helper == "etiqueta" and len(call.args) >= 2:
            base = call.args[1]
        centro = (0.0, 0.0)
        if base is not None:
            v = _eval_vec(base)
            if v and v[0] == "vec":
                centro = v[1]
            else:
                continue  # no evaluable: el rig lo encuadra en runtime
        for mov, expr in moves:
            if expr is None:
                continue
            v = _eval_vec(expr)
            if not v or v[0] != "vec":
                centro = None
                break
            if mov == "move_to":
                centro = v[1]
            else:
                centro = (centro[0] + v[1][0], centro[1] + v[1][1])
        if centro is None:
            continue
        w = min(am, max(1.0, len(texto) * fs * 0.009)) + d["pad"]
        h = fs * 0.02 + d["pad"]
        cajas.append((helper, centro, w, h))
    return cajas


def _cajas_prota(tree):
    """Cajas del protagonista: (centro, w, h) desde pos/altura."""
    cajas = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        nm = _nombre_llamada(node)
        if nm == "protagonista":
            pos = _kw(node, "pos", posicional=0, default=None)
            alt = _num(_kw(node, "altura", posicional=2, default=None), 3.0)
        elif nm == "version_prota":
            pos = _kw(node, "pos", posicional=1, default=None)
            alt = _num(_kw(node, "altura", posicional=2, default=None), 3.0)
        else:
            continue
        if pos is None:
            continue
        v = _eval_vec(pos)
        if not v or v[0] != "vec":
            continue
        px, py = v[1]
        cajas.append(((px, py + alt / 2), 0.5 * alt, alt))
    return cajas


def _checar_solape_texto(tree):
    """Ningún callout/etiqueta puede tapar al protagonista.

    El rig ya impide que salgan del encuadre (_Seguro); aquí se valida
    que no se encimen con el conductor de la escena.
    """
    protas = _cajas_prota(tree)
    if not protas:
        return ""
    for helper, (cx, cy), w, h in _cajas_texto(tree):
        for (px, py), pw, ph in protas:
            if abs(cx - px) < (w + pw) / 2 and abs(cy - py) < (h + ph) / 2:
                return (f"El {helper}() tapa al protagonista (centros a "
                        f"{abs(cx - px):.1f}/{abs(cy - py):.1f} unidades). "
                        f"Pon el {helper} al lado CONTRARIO del protagonista "
                        f"con pos= (p. ej. prota a la izquierda → "
                        f"{helper} con pos=RIGHT*3.4+UP*1), nunca encima.")
    return ""


def _checar_banda_vs_prota(tree):
    """La banda superior no puede tapar la cabeza del protagonista.

    Si hay banda_titulo()/titulo_seguro() y el protagonista queda con la
    cabeza dentro de la zona de la banda → error (cuenta como intento y se
    autorrepara). Solo se chequea cuando pos/altura son evaluables.
    """
    bandas, protas = [], []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        name = f.attr if isinstance(f, ast.Attribute) else (
            f.id if isinstance(f, ast.Name) else "")
        if name in ("banda_titulo", "titulo_seguro"):
            y = _num(_kw(node, "y", default=None), 2.55)
            bandas.append(y - 0.85)  # borde inferior de la banda
        elif name == "protagonista":
            pos = _kw(node, "pos", posicional=0, default=None)
            alt = _num(_kw(node, "altura", posicional=2, default=None), 3.0)
            protas.append((pos, alt))
        elif name == "version_prota":
            pos = _kw(node, "pos", posicional=1, default=None)
            alt = _num(_kw(node, "altura", posicional=2, default=None), 3.0)
            protas.append((pos, alt))
    if not bandas or not protas:
        return ""
    for pos_node, alt in protas:
        if pos_node is None:
            continue
        v = _eval_vec(pos_node)
        if not v or v[0] != "vec":
            continue  # no evaluable: no se puede probar, se deja pasar
        cabeza_top = v[1][1] + alt - 0.02  # como en el rig
        for borde in bandas:
            if cabeza_top > borde:
                return (f"La banda tapa la cabeza del protagonista "
                        f"(cabeza hasta y={cabeza_top:.2f}, la banda baja "
                        f"hasta y={borde:.2f}). Con banda arriba, el "
                        "protagonista va ABAJO: pos con y<=-1.2 y altura<=2.6 "
                        "(p. ej. pos=DOWN*1.2+LEFT*3.5, altura=2.6).")
    return ""


# Llamadas que pintan banda/título grande: solo UNA por escena (si no,
# se enciman, como pasó en producción).
_BANDAS = {"banda_titulo", "titulo_seguro", "title_card", "tarjeta_canal",
           "callout"}


def _validar_escena(code, cls):
    """Garantías por construcción del código de UNA escena.

    1) Usa el rig y define la clase pedida.
    2) El protagonista aparece (obligatorio en todas las escenas).
    3) UNA sola banda/título/callout (no se pueden encimar).
    Devuelve "" si pasa, o el mensaje de error (cuenta como intento y
    dispara la autorreparación con FIX_PROMPT).
    """
    if "zenn_rig" not in code or f"class {cls}" not in code:
        return (f"El código no usa el rig (falta 'from zenn_rig import *' o "
                f"la clase {cls}). Usa SOLO el rig para monigotes y props; "
                "no los construyas con Circle/Line sueltos.")
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"Error de sintaxis en el código: {e}"
    llamadas = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Attribute):
                llamadas.append(f.attr)
            elif isinstance(f, ast.Name):
                llamadas.append(f.id)
    if not any(n in ("protagonista", "version_prota") for n in llamadas):
        return ("Falta el protagonista: TODA escena debe incluir "
                "protagonista(...) o version_prota(n, ...) como conductor. "
                "Sin excepción.")
    bandas = [n for n in llamadas if n in _BANDAS]
    if len(bandas) > 1:
        return (f"La escena llama {len(bandas)} veces a banda/título "
                f"({', '.join(bandas)}): solo se permite UNA por escena "
                "porque se enciman. Quita las demás o usa etiqueta() para "
                "ideas secundarias.")
    # Layout: la banda no puede tapar la cabeza del protagonista.
    err_l = _checar_banda_vs_prota(tree)
    if err_l:
        return err_l
    # Layout: ningún callout/etiqueta puede tapar al protagonista.
    err_s = _checar_solape_texto(tree)
    if err_s:
        return err_s
    # Text() crudo gigante = texto cortado en bordes. Para títulos usar el
    # rig (banda_titulo/titulo_seguro/callout), que se auto-ajusta.
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            nm = f.attr if isinstance(f, ast.Attribute) else (
                f.id if isinstance(f, ast.Name) else "")
            if nm == "Text":
                fs = _num(_kw(node, "font_size", default=None), 48)
                if fs > 60:
                    return (f"Text() con font_size={fs:.0f} se sale de la "
                            "pantalla y se corta en los bordes. PROHIBIDO "
                            "font_size>60: usa banda_titulo(), "
                            "titulo_seguro(), callout() o etiqueta(), que se "
                            "auto-ajustan solos.")
            elif nm in ("callout", "etiqueta", "banda_titulo",
                        "titulo_seguro", "title_card"):
                fs = _num(_kw(node, "font_size", default=None), 0)
                if fs > 72:
                    return (f"{nm}() con font_size={fs:.0f} produce un "
                            "elemento gigante que tapa al protagonista. "
                            "PROHIBIDO font_size>72 en helpers de texto: usa "
                            "el tamaño por defecto (callout=60, etiqueta=40).")
    return ""


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


def _es_fallo_quota(err):
    return any(w in (err or "").lower() for w in
               ("rate limit", "quota", "429", "tokens per day", "tpd",
                "too many requests"))


def _generar_y_renderizar_escena(generate_fn, sdir, media, vdir, job, sc,
                                 rig_text, solo_render=False):
    """Genera (LLM) + valida + renderiza UNA escena, con autorreparación.

    solo_render=True: no llama al LLM (cero tokens); re-renderiza el
    scripts/{sid}.py que ya existe.
    Devuelve (ok: bool, err: str, es_quota: bool).
    """
    sid, cls = sc["id"], sc["id"].upper()
    out = vdir / f"{sid}.mp4"
    f = sdir / f"{sid}.py"
    adur = _probe_duration(job / "audio" / f"{sid}.mp3")
    secs = round(adur) if adur else max(4, len(sc["voz"].split()) // 3)
    code, err = None, ""
    intentos = 1 if solo_render else 3
    for intento in range(intentos):
        if solo_render:
            if not f.exists():
                return False, f"No hay código previo {sid}.py para re-renderizar.", False
            code = f.read_text(encoding="utf-8", errors="replace")
        else:
            try:
                if intento == 0:
                    prompt = SCENE_PROMPT.format(
                        cls=cls, rig=rig_text, sid=cls, voz=sc["voz"],
                        visual=sc["visual"] or sc["voz"][:80], secs=secs)
                    code, _ = generate_fn(
                        prompt, system="Eres programador experto en Manim. "
                                       "Devuelves solo código Python válido.")
                else:
                    fixed, _ = generate_fn(
                        FIX_PROMPT.format(error=err[-1500:], code=code,
                                          rig=rig_text),
                        system="Eres programador experto en Manim. "
                               "Devuelves solo código Python válido.")
                    code = fixed
            except Exception as e:
                err = str(e)
                break
        code = _strip_fences(code)
        # Validación por construcción: rig, protagonista y UNA sola banda.
        # No gastamos un render si no pasa; cuenta como intento.
        err = _validar_escena(code, cls)
        if err:
            continue
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
                vdur = _probe_duration(out)
                aviso = ""
                if adur and vdur < 0.3 * adur:
                    aviso = (f" AVISO: el video dura {vdur:.1f}s pero el audio "
                             f"{adur:.1f}s — el ensamblado rellenará con imagen "
                             "congelada; considera regenerar la escena.")
                return True, (f"render OK ({vdur:.1f}s)." + aviso), False
            err = "manim terminó sin generar el mp4."
        else:
            err = (r.stdout or "")[-1200:] + (r.stderr or "")[-1200:]
    return False, err, _es_fallo_quota(err)


def run_animacion(generate_fn, p, job, progress=None):
    """El LLM genera el código Manim escena por escena y lo renderiza.

    progress(stage, done, total, detalle): callback de avance con ETA.
    Con backend groq se pausa 6s entre escenas (OTPM 1000).
    """
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
    rig_text = _rig_api_text(sdir / "zenn_rig.py")

    prog = Progreso("animacion", progress)
    prog.start(len(scenes), "leyendo escenas")
    logs, arts, fallos = [], [], []
    fallos_quota = []  # escenas caídas por cuota del backend (no por código)
    # Estimación de consumo: el usuario debe dimensionar la cuota diaria.
    if getattr(generate_fn, "backend", "") == "groq":
        muestra = SCENE_PROMPT.format(cls="S00", rig=rig_text, sid="S00",
                                      voz="voz", visual="visual", secs=10)
        est = len(scenes) * (len(muestra) // 4 + 1200)
        logs.append(f"~{est // 1000}K tokens estimados en esta etapa "
                    f"({len(scenes)} escenas). Límite Groq gratuito: "
                    "200K/día. Si ya generaste guion+storyboard hoy, "
                    "reparte entre días o usa otro backend/Ollama local."
                    + (f" Con {len(scenes)} escenas NO cabe en un día: la "
                       "etapa se detendrá sola ante la cuota y reanudas "
                       "mañana (las hechas se omiten)." if est > 190000
                       else ""))
    done = 0
    paro_cuota, cls_cuota, det_cuota = False, "", ""
    for sc in scenes:
        sid, cls = sc["id"], sc["id"].upper()
        out = vdir / f"{sid}.mp4"
        if out.exists() and out.stat().st_size > 0:
            done += 1
            logs.append(f"{cls}: ya renderizada, se omite.")
            arts.append(str(out))
            prog.item(done, len(scenes), f"{cls} ya estaba")
            continue
        ok1, err, es_quota = _generar_y_renderizar_escena(
            generate_fn, sdir, media, vdir, job, sc, rig_text)
        if ok1:
            logs.append(f"{cls}: {err}")
            arts.append(str(out))
        else:
            fallos.append(cls)
            logs.append(f"{cls}: FALLO tras intentos: {err[-300:]}")
            if es_quota:
                # Cuota agotada: NO seguimos escena por escena fallando en
                # cascada ("brincando"). Se detiene la etapa aquí; reanudar
                # es un clic y las hechas se omiten solas.
                fallos_quota.append(cls)
                paro_cuota, cls_cuota = True, cls
                det_cuota = ("cuota DIARIA (TPD) agotada"
                             if any(w in err.lower()
                                    for w in ("tokens per day", "tpd"))
                             else "límite del backend (rate limit)")
                logs.append(f"⛔ {cls}: {det_cuota} — se DETIENE la etapa "
                            "aquí para no seguir fallando en cascada.")
                done += 1
                prog.item(done, len(scenes), f"{cls} cuota agotada")
                break
        done += 1
        prog.item(done, len(scenes),
                  f"{cls} lista" if ok1 else f"{cls} falló")
        if getattr(generate_fn, "backend", "") == "groq":
            time.sleep(6)  # OTPM 1000: no saturar tokens de salida/minuto
    # Estado real por escena: qué mp4 existe y qué huecos quedan.
    have = {p.stem.lower() for p in vdir.glob("*.mp4")
            if p.stat().st_size > 0}
    faltan = [s["id"].upper() for s in scenes if s["id"] not in have]
    n_have = len(scenes) - len(faltan)
    lista = ", ".join(faltan[:20]) + (f" …y {len(faltan) - 20} más"
                                      if len(faltan) > 20 else "")
    if paro_cuota:
        ok = False
        head = (f"⛔ Animación DETENIDA por cuota en {cls_cuota} "
                f"({det_cuota}): {n_have}/{len(scenes)} escenas con video. "
                f"Faltan {len(faltan)}: {lista}. No se siguió intentando "
                "para no quemar tiempo fallando en cascada."
                "\nOpciones: (1) reanuda cuando se resetee la cuota — las "
                "hechas se omiten solas; (2) cambia de backend en la barra "
                "lateral (Ollama local no tiene cuota); (3) si el proyecto "
                "tiene más escenas de las que caben en la cuota diaria, "
                "reparte la animación en 2 días.")
    elif not faltan:
        ok = True
        head = (f"Animación: {len(scenes)}/{len(scenes)} escenas "
                "renderizadas, sin huecos.")
    else:
        ok = False
        head = (f"Animación parcial: {n_have}/{len(scenes)} con video. "
                f"Faltan {len(faltan)}: {lista}. Reintenta la etapa o usa "
                "«Re-animar escena»; las ya hechas se omiten solas.")
    # Log completo persistente: cada ejecución queda en jobs/<id>/logs/
    # para revisarla después (el panel solo guarda la cola en la BD).
    logf = _guardar_log(job, "animacion", [head, "=" * 60] + logs)
    if logf:
        head += f"\n📄 Log completo de esta ejecución: {logf}"
    return ok, head + "\n" + "\n".join(logs[-25:]), arts, None


def run_reanimar_escena(generate_fn, p, job, sid, regen_code=True,
                        progress=None):
    """Re-anima UNA sola escena (p. ej. S07) sin tocar las demás.

    - Borra video/scenes/{sid}.mp4.
    - regen_code=True: borra también scripts/{sid}.py y regenera el código
      con el LLM (gasta tokens solo de esa escena), con validación y
      autorreparación.
    - regen_code=False: re-renderiza el scripts/{sid}.py existente
      (CERO tokens; útil si solo actualizaste el rig, p. ej. quitar mangas).
    Después hay que re-ejecutar la etapa 8 (Ensamblado) para regenerar el
    video final.
    """
    sid = sid.strip().lower()
    if not re.fullmatch(r"s\d+", sid):
        return False, f"Escena inválida: '{sid}'. Usa el formato S07.", [], None
    scenes = _parse_storyboard(job)
    sc = next((s for s in scenes if s["id"] == sid), None)
    if not sc:
        return (False, f"La escena {sid.upper()} no está en STORYBOARD.md.",
                [], None)
    rig = _rig_source()
    if not rig:
        return False, "No encuentro scripts/zenn_rig.py en el paquete.", [], None
    sdir = job / "scripts"
    sdir.mkdir(parents=True, exist_ok=True)
    (sdir / "zenn_rig.py").write_text(
        rig.read_text(encoding="utf-8"), encoding="utf-8")
    vdir = job / "video" / "scenes"
    vdir.mkdir(parents=True, exist_ok=True)
    media = job / "media"
    rig_text = _rig_api_text(sdir / "zenn_rig.py")
    out = vdir / f"{sid}.mp4"
    if out.exists():
        out.unlink()
    fpy = sdir / f"{sid}.py"
    if regen_code:
        if not generate_fn:
            return (False, "Regenerar código necesita un backend LLM "
                           "(Configuración) u Ollama local.", [], None)
        if fpy.exists():
            fpy.unlink()
    elif not fpy.exists():
        return (False, f"No hay código previo scripts/{sid}.py. Activa "
                       "'Regenerar código con LLM' o genera la escena en la "
                       "etapa 7.", [], None)
    prog = Progreso("reanimar", progress)
    prog.start(1, f"re-animando {sid.upper()}")
    ok1, err, es_quota = _generar_y_renderizar_escena(
        generate_fn, sdir, media, vdir, job, sc, rig_text,
        solo_render=not regen_code)
    prog.item(1, 1, f"{sid.upper()} lista" if ok1 else "falló")
    if ok1:
        log = (f"{sid.upper()}: {err}\n"
               "Ahora re-ejecuta la etapa 8 (Ensamblado) para regenerar el "
               "video final con esta escena corregida.")
        return True, log, [str(out)], None
    extra = ("\n⚠️ Fallo de CUOTA del backend, no de código." if es_quota else "")
    return False, f"{sid.upper()}: FALLO tras intentos: {err[-500:]}" + extra, [], None


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


def run_ensamblado(p, job, progress=None):
    """Une escenas + audios (el audio manda), SRT y versión subtitulada.

    progress(stage, done, total, detalle): callback de avance con ETA.
    """
    import shutil
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        return (False, "Falta ffmpeg/ffprobe en el PATH: instálalo para "
                       "poder ensamblar.", [], None)
    vdir = job / "video" / "scenes"
    scenes = sorted(vdir.glob("*.mp4")) if vdir.exists() else []
    if not scenes:
        return (False, "Sin videos de escenas: ejecuta antes la etapa 7 "
                       "(Animación).", [], None)
    # Garantía de duración: el video final debe cubrir TODAS las escenas del
    # storyboard. Si falta alguna, NO construimos un video corto en silencio:
    # fallamos con la lista para que se re-animen solo esas.
    sb_ids = [s["id"] for s in _parse_storyboard(job)]
    if sb_ids:
        have = {sc.stem.lower() for sc in scenes if sc.stat().st_size > 0}
        faltan = [i.upper() for i in sb_ids if i not in have]
        if faltan:
            return (False,
                    "Faltan los videos de estas escenas: "
                    + ", ".join(faltan) + ". El video final quedaría más "
                    "corto que la narración. Re-ejecuta la etapa 7 "
                    "(Animación: omite solas las ya hechas) o usa "
                    "«Re-animar escena» para cada una, y luego repite esta "
                    "etapa.", [], None)
    prog = Progreso("ensamblado", progress)
    prog.start(len(scenes) + 2, "leyendo escenas")
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
        vdur = _probe_duration(sc)
        aviso = (f" ⚠️ video {vdur:.1f}s < audio (relleno con imagen congelada)"
                 if vdur and vdur < 0.3 * adur else "")
        logs.append(f"{sid.upper()}: {adur:.1f}s{aviso}")
        prog.item(len(segs), len(scenes) + 2, f"{sid.upper()} unida")
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
    prog.item(len(segs) + 1, len(segs) + 2, "subtítulos generados")
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
    prog.item(len(segs) + 2, len(segs) + 2, "video final listo")
    log = (f"Ensamblado OK: {len(segs)} escenas, {total:.0f}s totales "
           f"({total / 60:.1f} min).\n" + " · ".join(logs) +
           ("\nVersión con subtítulos quemados generada."
            if r.returncode == 0 else
            "\nAVISO: no se pudo quemar subtítulos (revisa final.srt)."))
    logf = _guardar_log(job, "ensamblado", [log])
    if logf:
        log += f"\n📄 Log completo de esta ejecución: {logf}"
    return True, log, arts, None


# ---------- miniaturas (automático) ----------
THUMB_PROPS = ["reloj", "calendario", "cerebro", "tierra", "cohete",
               "bombilla", "corazon", "libro", "moneda", "pregunta", "agujero",
               "perro", "dino", "dragon", "curva", "lapida", "luna"]

_THUMB_EXPRS = {"sorpresa", "feliz", "preocupado"}
_THUMB_PLAYERAS = {"naranja", "azul", "verde", "roja", "amarilla", "rosa",
                   "teal", "morada", "negra", "blanca"}
# Expresión por defecto según tema (fallback sin LLM)
_EXPR_KEYWORDS = [
    (("miedo", "peligro", "tóxico", "toxinas", "veneno", "guerra",
      "terremoto", "apocalipsis", "desastre", "error"), "preocupado"),
    (("feliz", "felicidad", "amor", "éxito", "exito", "ganar", "récord",
      "record", "increíble", "increible"), "feliz"),
]


def _fallback_expr(title):
    t = title.lower()
    for keys, expr in _EXPR_KEYWORDS:
        if any(k in t for k in keys):
            return expr
    return "sorpresa"

THUMB_CONCEPT_PROMPT = """Eres diseñador de miniaturas de YouTube para un canal de divulgación científica.
Video: "{title}"
Propón 3 variantes. Cada variante: un TEXTO de 3-5 palabras en MAYÚSCULAS,
un OBJETO de esta lista exacta: {props}, una EXPRESION del protagonista
(sorpresa, feliz, preocupado — según la emoción del tema: misterio/peligro
→ preocupado, dato asombroso → sorpresa, dato positivo → feliz) y una
PLAYERA (naranja, azul, verde, roja, amarilla, rosa, teal, morada, negra,
blanca — varía por variante).
REGLA CLAVE: el TEXTO debe contener SIEMPRE el sustantivo o fenómeno
principal del título (p. ej. si el video es de un hoyo negro, el texto
debe decir HOYO NEGRO). Nunca cortes la frase antes de esa palabra.
Responde EXACTAMENTE así, sin texto extra:
VARIANTE 1
TEXTO: <...>
OBJETO: <...>
EXPRESION: <...>
PLAYERA: <...>
VARIANTE 2
TEXTO: <...>
OBJETO: <...>
EXPRESION: <...>
PLAYERA: <...>
VARIANTE 3
TEXTO: <...>
OBJETO: <...>
EXPRESION: <...>
PLAYERA: <...>
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
    """Devuelve 3 conceptos [{text, prop, expr, playera}]. LLM si hay;
    si no, heurística."""
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
                m_expr = re.search(r"EXPRESION:\s*(\w+)", block)
                m_play = re.search(r"PLAYERA:\s*(\w+)", block)
                if m_text:
                    prop = (m_prop.group(1).lower() if m_prop else "pregunta")
                    if prop not in THUMB_PROPS:
                        prop = "pregunta"
                    expr = (m_expr.group(1).lower() if m_expr
                            else "sorpresa")
                    if expr not in _THUMB_EXPRS:
                        expr = "sorpresa"
                    playera = (m_play.group(1).lower() if m_play
                               else "naranja")
                    if playera not in _THUMB_PLAYERAS:
                        playera = "naranja"
                    concepts.append({"text": m_text.group(1).strip()[:60],
                                     "prop": prop, "expr": expr,
                                     "playera": playera})
            if len(concepts) >= 3:
                return concepts[:3]
        except Exception:
            pass
    text, prop = _fallback_concept(title)
    expr = _fallback_expr(title)
    return [{"text": text, "prop": prop, "expr": expr, "playera": "naranja"},
            {"text": text, "prop": "pregunta", "expr": "sorpresa",
             "playera": "azul"},
            {"text": text, "prop": prop, "expr": expr, "playera": "verde"}]


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


def run_miniatura(generate_fn, p, progress=None):
    pid = p["id"]
    if progress:
        progress("miniatura", 0, 3, "generando conceptos")
    ok, log = run_thumbnails(pid, p["title"], generate_fn)
    if not ok:
        return False, log, [], None
    if progress:
        progress("miniatura", 3, 3, "3 variantes listas")
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
        au = job / "audio" / f"{it['id'].lower()}.mp3"
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
_NO_LLM = ("Esta etapa necesita un modelo: elige un backend en el sidebar "
           "y pon su API key en Configuración (o usa Ollama local).")


def _wrap_generate_fn(generate_fn, p, stage):
    """Envuelve generate_fn para registrar tokens en el Medidor.

    Lee llm.LAST_USAGE después de cada llamada y lo guarda en
    BASE/usage.jsonl. Si algo falla, no interrumpe la etapa.
    """
    def fn(prompt, system=""):
        text, model = generate_fn(prompt, system=system)
        try:
            import llm as _llm
            import usage as _usage
            u = getattr(_llm, "LAST_USAGE", None) or {}
            _usage.record(
                BASE, p.get("id"), p.get("title", ""), stage,
                u.get("backend") or getattr(generate_fn, "backend", ""),
                model, u.get("prompt_tokens"),
                u.get("completion_tokens"),
                estimado=u.get("estimado", False))
        except Exception:
            pass
        return text, model
    fn.backend = getattr(generate_fn, "backend", "")
    return fn


def execute_stage(p, stage, generate_fn=None, progress=None):
    """Devuelve (ok, log, artefactos, estado_sugerido|None).

    progress(stage, done, total, detalle): callback de avance con ETA
    para las etapas largas (tts, animación, ensamblado, miniaturas).
    """
    job = job_dir_of(p)
    kind = pget(p, "kind", "largo")
    if generate_fn is not None:
        generate_fn = _wrap_generate_fn(generate_fn, p, stage)
    try:
        if stage == "investigacion":
            return run_investigacion(generate_fn, p["title"], job)
        if stage == "guion":
            return run_guion_draft(generate_fn, p, job, kind)
        if stage == "verificacion":
            sp = find_script(p)
            if not sp:
                return False, "Sin guion para verificar.", [], None
            gtext = Path(sp).read_text(encoding="utf-8")
            dois, pmids = extract_references(gtext)
            # Aviso ortográfico: è/ò/à/ù no existen en español (típico
            # error del LLM que luego se quema en los subtítulos).
            sospechosas = sorted(set(re.findall(
                r"[A-Za-zÁÉÍÓÚáéíóúñÑ]*[èòàù][A-Za-zÁÉÍÓÚáéíóúñÑ]*", gtext)))
            log = (f"DOIs: {len(dois)}, PMIDs: {len(pmids)}\n" +
                   "\n".join(dois + [f"PMID:{x}" for x in pmids]))
            if sospechosas:
                log += ("\n\n⚠️ POSIBLES ERRORES DE TILDE (revísalos en el "
                        "guion antes del TTS): " + ", ".join(sospechosas[:20]))
            return True, log, [], None
        if stage == "storyboard":
            return run_storyboard(generate_fn, p, job)
        if stage == "tts":
            return run_tts_stage(p, job, progress=progress)
        if stage == "animacion":
            return run_animacion(generate_fn, p, job, progress=progress)
        if stage == "ensamblado":
            return run_ensamblado(p, job, progress=progress)
        if stage == "miniatura":
            return run_miniatura(generate_fn, p, progress=progress)
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


def run_all(conn, p, generate_fn, on_step=None, on_progress=None):
    """Ejecuta las etapas EN ORDEN y se detiene donde hace falta un humano.

    on_step(stage, ok, log) se llama tras cada etapa ejecutada.
    on_progress(stage, done, total, detalle) reporta el avance de las
    etapas largas con ETA.
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
                ok, log, arts, sugg = execute_stage(p, name, generate_fn,
                                                   progress=on_progress)
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
        ok, log, arts, sugg = execute_stage(p, name, generate_fn,
                                                   progress=on_progress)
        _db.set_stage(conn, pid, name,
                      sugg or ("ok" if ok else "fallo"), log, arts)
        if on_step:
            on_step(name, ok, log)
        if not ok:
            return "error", name
    return "done", ""


# ---------- propuestas de temas (asistida por LLM) ----------
TOPIC_PROMPT = """Propón 8 temas para videos de curiosidad del canal "El Porqué"
(español neutro): una sola pregunta por video, 8-12 minutos, animación de
dibujos simples con personaje cabezón de playera naranja. Público:
hispanohablantes curiosos. El formato "curiosidad animada" en español está
casi vacío: tenemos ventaja si los títulos y ángulos son mejores que los
canales top en inglés (Ink Explainer, Simple Paint, theblurb).

MEZCLA estos 5 tipos:
- 3 CURIOSIDADES CIENTÍFICAS con hueco de curiosidad (datos que rompen una
  creencia común; la ciencia real citada después es nuestra ventaja).
- 2 de CULTURA ALTERNATIVA: lo que cree la cultura popular / mitos /
  historia poco contada, contrastado con lo que dice la ciencia.
- 1 PREGUNTA COTIDIANA con respuesta sorprendente ("¿por qué...?" de la
  vida diaria que nadie se había planteado).
- 1 EXPERIMENTO MENTAL "¿Qué pasaría si...?" (formato serie de alto
  rendimiento: ej. "¿Qué pasaría si la Tierra fuera del tamaño de Júpiter?").
- 1 de SERIE "EN CADA NIVEL DE X": formato infinito y adictivo
  (ej: "¿Cómo es el frío en cada nivel de temperatura?", "Tu cuerpo en
  cada nivel de falta de sueño").

FÓRMULAS DE TÍTULO QUE VENDEN (úsalas, en español):
a) Pregunta directa con hueco: "¿Qué hacían los humanos hace 10,000 años
   todo el día?" (8M vistas en el referente).
b) Segunda persona + secreto: "¿Por qué X? (casi nadie lo sabe)".
c) Cifra + punto de quiebre: "¿Qué cambia en tu cuerpo después de 24 horas
   sin dormir?".
d) Supervivencia con stakes: "¿Cómo sobrevivieron los humanos a inviernos
   que debieron matarlos?".
e) Superlativo honesto (NADA morboso: sin muertes ni desastres): "El peor
   error científico de la historia".
f) Comportamiento animal: "¿Entienden los animales la muerte?".

REGLAS: palabra clave al frente, promesa concreta, nada de títulos vagos.
Nada de morbo (muertes/desastres): nuestro posicionamiento es credibilidad.

Para cada tema devuelve EXACTAMENTE este formato, sin texto extra:

PREGUNTA: <la pregunta del video, ya como título>
FORMULA: <qué fórmula usa: a/b/c/d/e/f>
ANGULO: <1 línea: por qué engancha / qué creencia rompe>
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
