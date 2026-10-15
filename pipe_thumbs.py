"""Miniaturas: conceptos LLM, generacion de PNG y etapa 9."""
import json
import re
import sys
from pathlib import Path

from pipe_core import BASE, HERE, run

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
