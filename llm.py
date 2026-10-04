#!/usr/bin/env python3
"""Router multi-backend de LLMs del panel Zenn Factory.

Backends con capa gratuita verificada 2026-09/10; catálogos de modelos
gratuitos renovados en vivo el 2026-10-03 (solo ids gratis por
plataforma, DeepSeek es el único backend de pago). Los sets gratuitos
rotan en todos los proveedores; el orden de cada cadena es preferencia,
no garantía de disponibilidad. Si un modelo falla (404/429/límite),
se intenta el siguiente automáticamente.

  gemini     Google AI Studio — ~1.500 req/día en Flash, sin tarjeta.
  groq       OpenAI-compatible — rapidísimo (300-1000 tok/s).
  cerebras   OpenAI-compatible — ~1M tok/día, el más rápido; lineup rotativo.
  openrouter Agregador :free — 50 req/día (1.000 con $10 de crédito).
  mistral    La Plateforme plan "Experiment" — cuota mensual muy alta.
             OJO: el gratis exige aceptar que Mistral entrene con tus datos.
  cohere     Trial key — 1.000 llamadas/mes.
  tokenharbor Solo los modelos GRATIS del catálogo (ids que terminan en
             `:free`; el resto cargan saldo y aquí no se muestran).
  freellmapi  FreeLLMAPI — GLM/Qwen/Kimi con la bolsa de tokens gratis
             (10.000 al crear la key).
  deepseek   DeepSeek oficial (api.deepseek.com) — de pago, con tu key.
  ollama     Modelos locales vía http://localhost:11434 (lista dinámica
             con `ollama list` — aparece lo que Chino tenga instalado).

Nada aquí garantiza un guion "perfecto": la calidad sale del proceso
(PROMPT_MAESTRO -> borrador -> pasada de crítico -> aprobación humana).

Sin dependencias extra: todo va por urllib (REST directo).
"""
import json
import re
import time
import urllib.request
import urllib.error

# ---------- catálogo ----------
BACKENDS = {
    "gemini":     {"label": "Gemini · Google AI Studio",
                   "setting": "gemini_key", "env": "GEMINI_API_KEY",
                   "free": "~1.500 req/día (Flash), sin tarjeta"},
    "groq":       {"label": "Groq",
                   "setting": "groq_key", "env": "GROQ_API_KEY",
                   "free": "1.000 req/día y 200K tok/día por modelo"},
    "cerebras":   {"label": "Cerebras",
                   "setting": "cerebras_key", "env": "CEREBRAS_API_KEY",
                   "free": "~1M tok/día, lineup rotativo"},
    "openrouter": {"label": "OpenRouter :free",
                   "setting": "openrouter_key", "env": "OPENROUTER_API_KEY",
                   "free": "50 req/día (1.000 con $10 de crédito)"},
    "mistral":    {"label": "Mistral · La Plateforme",
                   "setting": "mistral_key", "env": "MISTRAL_API_KEY",
                   "free": "plan Experiment (~1B tok/mes); aceptas training"},
    "cohere":     {"label": "Cohere (trial)",
                   "setting": "cohere_key", "env": "COHERE_API_KEY",
                   "free": "1.000 llamadas/mes con trial key"},
    "tokenharbor": {"label": "Token Harbor · solo gratis",
                    "setting": "tokenharbor_key", "env": "TOKENHARBOR_API_KEY",
                    "free": "solo ids `:free` (7×24h por cuenta)"},
    "freellmapi": {"label": "FreeLLMAPI · gratis",
                   "setting": "freellmapi_key", "env": "FREELLMAPI_API_KEY",
                   "free": "10.000 tokens al crear la key"},
    "deepseek":   {"label": "DeepSeek · oficial",
                   "setting": "deepseek_key", "env": "DEEPSEEK_API_KEY",
                   "free": "de pago (tarifa por token)"},
    "ollama":     {"label": "Ollama · local",
                   "setting": "", "env": "",
                   "free": "ilimitado (tu hardware)"},
}

# Orden de preferencia para el combo (calidad ES + cuota + velocidad).
BACKEND_ORDER = ["gemini", "groq", "tokenharbor", "freellmapi", "deepseek",
                 "cerebras", "openrouter", "mistral", "cohere", "ollama"]

# FreeLLMAPI: por defecto el router LOCAL (start-all.bat, puerto 3001).
# Si prefieres el hosted, cambia esta URL en Configuración.
FREELLMAPI_BASE = "http://localhost:3001/v1"

# Endpoints OpenAI-compatibles
OPENAI_BASES = {
    "groq": "https://api.groq.com/openai/v1",
    "cerebras": "https://api.cerebras.ai/v1",
    "mistral": "https://api.mistral.ai/v1",
    "tokenharbor": "https://tokenharbor.ai/v1",
    "freellmapi": FREELLMAPI_BASE,
    "deepseek": "https://api.deepseek.com/v1",
}

# Backends en los que SOLO se muestran/generan ids con este sufijo:
# lo demás del catálogo es de pago y no queremos gastar saldo.
# (Catálogos verificados en vivo el 2026-10-03.)
FREE_ONLY = {"tokenharbor": ":free", "openrouter": ":free"}

# Alias que no terminan en el sufijo pero también son gratis y hay que
# conservar en la cadena (el meta-router de OpenRouter).
FREE_KEEP = {"openrouter": {"openrouter/free"}}

# Alias del router FreeLLMAPI: `auto` deja que su router elija el mejor
# modelo gratis disponible (auto:smart/auto:fast/auto:cheap = prioridades).
ROUTER_ALIASES = {"freellmapi": ["auto", "auto:smart", "auto:fast",
                                 "auto:cheap"]}

# Catálogos enormes (FreeLLMAPI trae cientos de ids): el combo se queda
# con alias + preferidos + hasta MODEL_CAP descubiertos.
MODEL_CAP = {"freellmapi": 60}


def _base(backend, keys=None):
    """Base URL del backend (FreeLLMAPI es configurable por la UI)."""
    if backend == "freellmapi":
        return (keys or {}).get("freellmapi_base") or FREELLMAPI_BASE
    return OPENAI_BASES[backend]
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Cadenas de preferencia (se intersectan con lo descubierto vía /models
# cuando hay key; si el descubrimiento falla, se prueban en este orden).
# Solo modelos GRATIS por plataforma; DeepSeek queda como único de pago.
PREFERRED = {
    "gemini": ["gemini-2.5-flash", "gemini-flash-latest", "gemini-3.5-flash",
               "gemini-3.8-flash", "gemini-2.5-flash-lite"],
    "groq": ["openai/gpt-oss-120b", "openai/gpt-oss-20b",
             "qwen/qwen3.8-27b", "llama-3.3-70b-versatile"],
    "cerebras": ["zai-glm-4.7", "gpt-oss-120b", "llama-3.3-70b"],
    "openrouter": [
        "qwen/qwen3.8-27b:free",
        "nvidia/nemotron-3-super-120b-a12b:free",
        "google/gemma-4-31b-it:free",
        "thinkingmachines/inkling:free",
        "nvidia/nemotron-3-ultra-550b-a55b:free",
        "openrouter/free",  # meta-router: elige un :free disponible
    ],
    "mistral": ["mistral-small-latest", "mistral-medium-latest",
                "magistral-small-latest", "ministral-14b-latest"],
    "cohere": ["command-a-03-2025", "command-r-plus", "command-r"],
    # Solo ids gratuitos: con la key, resolve_chain() los sustituye por
    # los que devuelva /models filtrando el mismo sufijo.
    "tokenharbor": ["deepseek-v4.1-flash:free", "qwen3.8-flash:free",
                    "mimo-v2.6-flash:free", "deepseek-v4-flash:free",
                    "mimo-v2.5:free"],
    "freellmapi": ["gemini-2.5-flash", "glm-4.7", "kimi-k3",
                   "qwen3.8-flash", "deepseek-v4-flash"],
    # Único backend de pago (sin FREE_ONLY): ids vigentes 2026-10-03.
    "deepseek": ["deepseek-flash", "deepseek-v4-pro"],
}

OLLAMA_URL = "http://localhost:11434"


class LLMError(Exception):
    pass


# ---------- HTTP ----------
# Cloudflare (Groq) bloquea el User-Agent por defecto de urllib -> HTTP 403/1010.
_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/124.0 Safari/537.36"}


def _post_json(url, payload, headers=None, timeout=300):
    data = json.dumps(payload).encode()
    hdrs = dict(_UA)
    hdrs.update(headers or {})
    hdrs.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:300]
        raise LLMError(f"HTTP {e.code}: {body}")
    except Exception as e:
        raise LLMError(str(e))


def _get_json(url, headers=None, timeout=30):
    hdrs = dict(_UA)
    hdrs.update(headers or {})
    req = urllib.request.Request(url, headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        raise LLMError(str(e))


# ---------- ollama ----------
def list_ollama_models(timeout=5):
    """Devuelve [nombres] de `ollama list` vía API. [] si no hay servidor."""
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode())
        return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []


def _ollama_generate(model, prompt, system=""):
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system,
        "stream": False,
        # Modelos híbridos (qwen3.x/gemma4): sin esto se "piensen" la
        # respuesta entera en el canal de razonamiento y content sale vacío.
        "think": False,
        "options": {"temperature": 0.7, "num_ctx": 8192},
    }
    try:
        out = _post_json(f"{OLLAMA_URL}/api/generate", payload, timeout=600)
    except LLMError as e:
        if "think" not in str(e).lower():
            raise LLMError(f"Ollama no responde en {OLLAMA_URL} ({e}). "
                           "¿Está corriendo `ollama serve`?")
        payload.pop("think", None)   # modelo sin modo razonamiento
        try:
            out = _post_json(f"{OLLAMA_URL}/api/generate", payload,
                             timeout=600)
        except LLMError as e2:
            raise LLMError(f"Ollama no responde en {OLLAMA_URL} ({e2}). "
                           "¿Está corriendo `ollama serve`?")
    text = (out.get("response") or "").strip()
    if not text and out.get("thinking"):
        raise LLMError("El modelo local solo devolvió razonamiento "
                       "(vacío). Elige otro modelo o ponlo en modo no "
                       "pensante.")
    return text


# Límite de salida por minuto (OTPM) de Groq: pedir más de 1.000 tokens
# de golpe devuelve 400 aunque el modelo lo necesite. El resto de backends
# usan el máximo por defecto.
MAX_TOKENS = {"groq": 1200}  # OTPM 1000: ~1200 tokens ≈ escenas compactas sin truncar


def _rate_kind(msg):
    """Clasifica un error de cuota: 'wait' (se libera solo, reintentar),
    'skip' (cuota diaria/facturación: saltar al siguiente modelo),
    None (no es cuota)."""
    m = (msg or "").lower()
    if "too large for model" in m:
        return None   # error duro de cuota: reintentar no arregla nada
    skip = ("exceeded your current quota", "quota exceeded",
            "daily quota", "check your plan", "billing",
            "resource_exhausted", "insufficient_quota", "insufficient funds",
            "account", "suspend")
    if any(p in m for p in skip):
        return "skip"
    wait = ("rate limit", "too many requests", " 429",
            "output tokens per minute", "requests per minute",
            "tokens per minute", "try again", "temporarily",
            "overloaded", "server busy")
    if any(p in m for p in wait):
        return "wait"
    return None


def _is_rate_limit(msg):
    return _rate_kind(msg) is not None


def _rate_wait(msg, default=30.0):
    """Segundos que el proveedor pide esperar (o el default)."""
    m = re.search(r"(?:try again in|in)\s+(\d+(?:\.\d+)?)s", msg or "")
    if m:
        return min(float(m.group(1)) + 2.0, 120.0)
    m = re.search(r"retry in (\d+(?:\.\d+)?)", msg or "")
    if m:
        return min(float(m.group(1)) + 2.0, 120.0)
    return default


# ---------- openai-compatible (groq / cerebras / mistral) ----------
def _openai_chat(base, api_key, model, prompt, system="",
                 max_tokens=8192):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    out = _post_json(
        f"{base}/chat/completions",
        {"model": model, "messages": messages,
         "temperature": 0.7, "max_tokens": max_tokens},
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key}"},
    )
    try:
        return out["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        raise LLMError(f"Respuesta inesperada de {model}: {str(out)[:200]}")


def _openai_models(base, api_key):
    """Descubre modelos vía GET {base}/models. [] si falla."""
    try:
        out = _get_json(f"{base}/models",
                        headers={"Authorization": f"Bearer {api_key}"})
        return [m["id"] for m in out.get("data", []) if m.get("id")]
    except LLMError:
        return []


# ---------- openrouter ----------
def _openrouter_generate(model, prompt, system, api_key):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    out = _post_json(
        OPENROUTER_URL,
        {"model": model, "messages": messages, "temperature": 0.7},
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key}"},
        timeout=300,
    )
    try:
        return out["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        raise LLMError(f"Respuesta inesperada de {model}: {str(out)[:200]}")


# ---------- gemini (REST directo, sin SDK) ----------
def _gemini_generate(api_key, model, prompt, system=""):
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192},
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    out = _post_json(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}"
        f":generateContent?key={api_key}",
        body,
    )
    try:
        parts = out["candidates"][0]["content"]["parts"]
        return "".join(p.get("text", "") for p in parts).strip()
    except (KeyError, IndexError, TypeError):
        raise LLMError(f"Respuesta inesperada de {model}: {str(out)[:200]}")


def _gemini_models(api_key):
    """Descubre modelos vía ListModels. [] si falla."""
    try:
        out = _get_json(
            "https://generativelanguage.googleapis.com/v1beta/models"
            f"?key={api_key}")
        ids = []
        for m in out.get("models", []):
            name = (m.get("name") or "").replace("models/", "")
            if "generateContent" in (m.get("supportedGenerationMethods") or []):
                ids.append(name)
        return ids
    except LLMError:
        return []


# ---------- cohere (v1/chat) ----------
def _cohere_chat(api_key, model, prompt, system=""):
    body = {"model": model, "message": prompt, "temperature": 0.7,
            "max_tokens": 4096}
    if system:
        body["preamble"] = system
    out = _post_json(
        "https://api.cohere.com/v1/chat", body,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key}"},
    )
    text = out.get("text")
    if not text:
        raise LLMError(f"Respuesta inesperada de {model}: {str(out)[:200]}")
    return text.strip()


# ---------- resolución de cadena ----------
def resolve_chain(backend, model, keys):
    """Modelos a intentar, en orden. `model` explícito va primero y solo."""
    if model:
        return [model]
    key = (keys or {}).get(backend, "")
    if key and backend in OPENAI_BASES:
        found = _openai_models(_base(backend, keys), key)
        if backend in FREE_ONLY:  # solo ids gratuitos (p.ej. `:free`)
            suf = FREE_ONLY[backend]
            keep = FREE_KEEP.get(backend, set())
            found = [m for m in found if m.endswith(suf) or m in keep]
        if found:
            pref = PREFERRED[backend]
            ok = [m for m in pref if m in found]
            chain = ok + [m for m in found if m not in pref][:2]
            if backend in MODEL_CAP:  # catálogo enorme: alias + tope
                alias = list(ROUTER_ALIASES.get(backend, ()))
                rest = [m for m in found if m not in ok][
                    :max(0, MODEL_CAP[backend] - len(alias) - len(ok))]
                chain = alias + ok + rest
            return chain
    if key and backend == "gemini":
        found = _gemini_models(key)
        if found:
            pref = PREFERRED["gemini"]
            return [m for m in pref if m in found] + \
                   [m for m in found if "flash" in m.lower()][:2]
    return list(PREFERRED.get(backend, []))


def generate(prompt, backend="gemini", model="", system="", keys=None,
             api_key=""):
    """Genera texto. Devuelve (texto, modelo_usado).

    keys: dict {"gemini": "...", "groq": "...", ...}. `api_key` es el
    legado de openrouter (se respeta si keys no lo trae).
    Recorre la cadena del backend hasta que un modelo responda.
    """
    keys = dict(keys or {})
    if api_key and "openrouter" not in keys:
        keys["openrouter"] = api_key
    if backend not in BACKEND_ORDER:
        raise LLMError(f"Backend desconocido: {backend}")

    if backend == "ollama":
        if not model:
            raise LLMError("Elige un modelo local en el combo.")
        return _ollama_generate(model, prompt, system), model

    key = keys.get(backend, "")
    if not key:
        raise LLMError(
            f"Falta {BACKENDS[backend]['env']} para el backend "
            f"'{BACKENDS[backend]['label']}'. Ponla en Configuración.")

    chain = resolve_chain(backend, model, keys)
    max_tokens = MAX_TOKENS.get(backend, 8192)
    errors = []
    for m in chain:
        for attempt in range(3):  # 3 intentos si el proveedor pide esperar
            try:
                if backend == "gemini":
                    text = _gemini_generate(key, m, prompt, system)
                elif backend == "cohere":
                    text = _cohere_chat(key, m, prompt, system)
                elif backend == "openrouter":
                    text = _openrouter_generate(m, prompt, system, key)
                else:  # groq, cerebras, mistral, tokenharbor, freellmapi,
                        # deepseek
                    text = _openai_chat(_base(backend, keys), key, m,
                                        prompt, system,
                                        max_tokens=max_tokens)
                if not text:
                    raise LLMError("respuesta vacía")
                return text, m
            except LLMError as e:
                kind = _rate_kind(str(e))
                if kind == "wait" and attempt < 2:
                    wait = _rate_wait(str(e))
                    time.sleep(wait)   # cuota por minuto: se libera sola
                    continue
                if kind == "skip":
                    errors.append(f"{m}: cuota agotada, salto al siguiente "
                                  f"modelo ({e})")
                    break              # no tiene caso reintentar el mismo
                errors.append(f"{m}: {e}")
                break
    raise LLMError(f"Ningún modelo de '{backend}' respondió.\n" +
                   "\n".join(errors))


def backend_options():
    return list(BACKEND_ORDER)


def model_options(backend, keys=None):
    """Opciones para el combo según backend (descubrimiento si hay key)."""
    if backend == "ollama":
        # Fuera modelos de embeddings: no sirven para chat/guiones.
        return [m for m in list_ollama_models() if "embed" not in m.lower()]
    if backend in BACKEND_ORDER:
        return resolve_chain(backend, "", keys or {})
    return []
