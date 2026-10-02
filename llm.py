#!/usr/bin/env python3
"""Router multi-backend de LLMs del panel Zenn Factory.

Backends con capa gratuita verificada 2026-09/10. Los sets gratuitos
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
  ollama     Modelos locales vía http://localhost:11434 (lista dinámica
             con `ollama list` — aparece lo que Chino tenga instalado).

Nada aquí garantiza un guion "perfecto": la calidad sale del proceso
(PROMPT_MAESTRO -> borrador -> pasada de crítico -> aprobación humana).

Sin dependencias extra: todo va por urllib (REST directo).
"""
import json
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
    "ollama":     {"label": "Ollama · local",
                   "setting": "", "env": "",
                   "free": "ilimitado (tu hardware)"},
}

# Orden de preferencia para el combo (calidad ES + cuota + velocidad).
BACKEND_ORDER = ["gemini", "groq", "cerebras", "openrouter",
                 "mistral", "cohere", "ollama"]

# Endpoints OpenAI-compatibles
OPENAI_BASES = {
    "groq": "https://api.groq.com/openai/v1",
    "cerebras": "https://api.cerebras.ai/v1",
    "mistral": "https://api.mistral.ai/v1",
}
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Cadenas de preferencia (se intersectan con lo descubierto vía /models
# cuando hay key; si el descubrimiento falla, se prueban en este orden).
PREFERRED = {
    "gemini": ["gemini-2.5-flash", "gemini-2.0-flash", "gemma-3-27b-it"],
    "groq": ["qwen/qwen3.8-27b", "openai/gpt-oss-120b", "openai/gpt-oss-20b"],
    "cerebras": ["zai-glm-4.7", "gpt-oss-120b", "llama-3.3-70b"],
    "openrouter": [
        "nvidia/nemotron-3-super-120b-a12b:free",
        "google/gemma-4-31b-it:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "openrouter/free",  # meta-router: elige un :free disponible
    ],
    "mistral": ["mistral-small-latest", "mistral-medium-latest",
                "mistral-large-latest", "open-mistral-7b"],
    "cohere": ["command-a-03-2025", "command-r-plus", "command-r"],
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
        "options": {"temperature": 0.7, "num_ctx": 8192},
    }
    try:
        out = _post_json(f"{OLLAMA_URL}/api/generate", payload, timeout=600)
    except LLMError as e:
        raise LLMError(f"Ollama no responde en {OLLAMA_URL} ({e}). "
                       "¿Está corriendo `ollama serve`?")
    return (out.get("response") or "").strip()


# ---------- openai-compatible (groq / cerebras / mistral) ----------
def _openai_chat(base, api_key, model, prompt, system=""):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    out = _post_json(
        f"{base}/chat/completions",
        {"model": model, "messages": messages,
         "temperature": 0.7, "max_tokens": 8192},
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key}"},
    )
    try:
        return out["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        raise LLMError(f"Respuesta inesperada de {model}: {str(out)[:200]}")


# Modelos que NO sirven para escribir (ASR, guardia, embeddings, TTS).
_NON_CHAT = ("whisper", "prompt-guard", "orpheus", "safeguard", "embed",
             "embedding", "moderation")


def _openai_models(base, api_key):
    """Descubre modelos vía GET {base}/models. [] si falla."""
    try:
        out = _get_json(f"{base}/models",
                        headers={"Authorization": f"Bearer {api_key}"})
        return [m["id"] for m in out.get("data", []) if m.get("id")
                and not any(b in m["id"].lower() for b in _NON_CHAT)]
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
        found = _openai_models(OPENAI_BASES[backend], key)
        if found:
            pref = PREFERRED[backend]
            return [m for m in pref if m in found] + \
                   [m for m in found if m not in pref][:2]
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
    errors = []
    for m in chain:
        try:
            if backend == "gemini":
                text = _gemini_generate(key, m, prompt, system)
            elif backend == "cohere":
                text = _cohere_chat(key, m, prompt, system)
            elif backend == "openrouter":
                text = _openrouter_generate(m, prompt, system, key)
            else:  # groq, cerebras, mistral
                text = _openai_chat(OPENAI_BASES[backend], key, m,
                                    prompt, system)
            if not text:
                raise LLMError("respuesta vacía")
            return text, m
        except LLMError as e:
            errors.append(f"{m}: {e}")
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
