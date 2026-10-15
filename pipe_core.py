"""Nucleo compartido del pipeline (v30): constantes de etapas, utilidades puras y prompts base.

Todos los modulos pipe_* importan de aqui; este no importa de ninguno.
"""
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

PANEL_VERSION = "v30"  # se muestra en el pie del sidebar; subir en cada release
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


# v29.1 — secciones del guion que NO se narran (no cuentan para cobertura).
_GUION_SECCION_NO_NARRADA = re.compile(
    r"^\s*#{1,6}\s*\**\s*(FUENTES|MINIATURAS|RECURSOS|CR[EÉ]DITOS|"
    r"NOTAS DE PRODUCCI|T[IÍ]TULOS|DESCRIPCI|TAGS|HASHTAGS|M[UÚ]SICA|"
    r"ANEXOS?)\b", re.IGNORECASE)
_GUION_LINEA_NO_NARRADA = re.compile(
    r"^\s*(\[VISUAL\b|\[IMAGEN\b|\[ESCENA\b|\[PLANO\b|#{1,6}\s|"
    r"---+$)", re.IGNORECASE)
_GUION_TIMECODE = re.compile(
    r"\(\s*\d{1,2}:\d{2}\s*[–\-—]\s*\d{1,2}:\d{2}\s*\)")


def _narracion_guion(text):
    """Devuelve SOLO la narración de un guion (lo que el TTS lee en voz alta).

    v29.1: la cobertura del storyboard se medía contra el guion CRUDO, que
    incluye el markup de producción (encabezados `## BLOQUE`, notas
    `[VISUAL: ...]`, timecodes `(0:30–2:00)` y las secciones FUENTES/
    MINIATURAS). Ese texto nunca se narra: cuenta palabras de más y vuelve el
    umento del 90% imposible, así que la etapa 5 marcaba un FALSO «STORYBOARD
    TRUNCADO» (proyecto 35: 1338 «palabras» cuando la narración real era
    ~1163) y partía el guion dejando una 3ª parte que era solo la sección
    FUENTES. Aquí se quita todo eso: el resultado es lo que se narra.
    """
    out = []
    skip = False
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if _GUION_SECCION_NO_NARRADA.match(s):
            skip = True            # FUENTES/MINIATURAS/...: fuera hasta el
            continue               # próximo encabezado
        if re.match(r"^\s*#{1,6}\s", s):
            skip = False           # encabezado de bloque narrativo: sigue
            continue
        if skip or _GUION_LINEA_NO_NARRADA.match(s):
            continue
        s = _GUION_TIMECODE.sub("", s).strip()
        if s:
            out.append(s)
    return "\n\n".join(out)


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
MIN_PALABRAS_GUION = 1300
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


def _es_fallo_quota(err):
    return any(w in (err or "").lower() for w in
               ("rate limit", "quota", "429", "tokens per day", "tpd",
                "too many requests"))


_NO_LLM = ("Esta etapa necesita un modelo: elige un backend en el sidebar "
           "y pon su API key en Configuración (o usa Ollama local).")


def _audio_path(job, sid):
    """ÚNICA forma válida de construir la ruta de un audio.

    v26: antes había 5+ construcciones inline de job/"audio"/f"{id}.mp3"
    repartidas entre TTS, verificación, reparación y ensamblado. Si alguna
    normalizaba distinto, el TTS podía "omitir por existente" un archivo que
    el ensamblado no encontraba. Ahora todos usan esta función.
    """
    return Path(job) / "audio" / f"{str(sid).lower()}.mp3"


