"""Etapas asistidas de guion: investigacion, borrador con critico y expansion."""
import json
import re
import time
from pathlib import Path

from pipe_core import (BASE, MIN_PALABRAS_GUION, count_words, estimate_minutes,
                       prompt_maestro, run)

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


# Mínimo estructural del canal: 8 min ≈ 1300 palabras a 155 ppm.
# Un guion más corto produce un video corto (fuga detectada en jobs/27 y 32).
def expandir_guion(generate_fn, guion_actual, research=""):
    """Expande un guion corto hasta el mínimo del canal (hasta 2 intentos).

    Devuelve (texto_final, palabras). No falla en silencio: si tras los
    intentos sigue corto, la Puerta 1 bloquea la aprobación.
    """
    texto, model, _ = guion_actual, "", 0
    for intento in range(2):
        palabras = count_words(texto)
        if palabras >= MIN_PALABRAS_GUION:
            break
        faltan = MIN_PALABRAS_GUION - palabras
        prompt = (
            f"Este guion tiene {palabras} palabras de narración y necesita "
            f"mínimo {MIN_PALABRAS_GUION} (faltan ~{faltan}). "
            f"EXPÁNDELO: añade datos, ejemplos y contexto de la investigación, "
            f"desarrolla los bloques más cortos y, si hace falta, agrega un "
            f"bloque nuevo antes del cierre. PROHIBIDO repetir información o "
            f"rellenar con paja: cada frase nueva debe aportar un dato real. "
            f"Mantén saludo fijo, hook, picos y despedida fija. Devuelve el "
            f"guion COMPLETO (no solo lo añadido), en español.\n\n"
            f"GUION ACTUAL:\n{texto[:14000]}"
            + (f"\n\nINVESTIGACIÓN:\n{research[:4000]}" if research else ""))
        try:
            texto, model = generate_fn(
                prompt, system="Eres guionista de divulgación científica.")
        except Exception:
            break
    return texto, count_words(texto), model


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
    words = count_words(txt)
    expandio = ""
    if kind == "largo" and words < MIN_PALABRAS_GUION:
        txt, words, used = expandir_guion(generate_fn, txt, research)
        expandio = f" (expansión automática: {words} palabras)"
    out = job / "GUION.md"
    out.write_text(txt, encoding="utf-8")
    log = (f"Borrador con {used}: {words} palabras ≈ "
           f"{estimate_minutes(words):.1f} min.{expandio}\n"
           "PENDIENTE: léelo abajo y apruébalo en la Puerta 1.")
    # Ojo: estado 'en-curso' — la etapa solo se cierra con tu aprobación.
    return True, log, [str(out)], "en-curso"
