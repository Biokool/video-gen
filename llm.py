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
  cloudflare Cloudflare Workers AI (plan Free: 10.000 neuronas/día).
             21 ids `@cf/...` verificados en vivo el 2026-10-04; el resto
             del catálogo no corre en plan Free (se filtra solo).
  nvidia     NVIDIA API catalog (build.nvidia.com) — 80 ids listados,
             10 responden en la cuenta (verificado en vivo el 2026-10-05):
             el resto da 404 "Not found for account" o se queda sin
             respuesta, y se descartan solos.
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
    "cloudflare": {"label": "Cloudflare · Workers AI",
                   "setting": "cloudflare_key", "env": "CLOUDFLARE_API_KEY",
                   "free": "plan Free: 10.000 neuronas/día (21 modelos OK)"},
    "nvidia":     {"label": "NVIDIA API · NIM",
                   "setting": "nvidia_key", "env": "NVIDIA_API_KEY",
                   "free": "API catalog: 10 de 80 ids responden (2026-10-05)"},
    "deepseek":   {"label": "DeepSeek · oficial",
                   "setting": "deepseek_key", "env": "DEEPSEEK_API_KEY",
                   "free": "de pago (tarifa por token)"},
    "ollama":     {"label": "Ollama · local",
                   "setting": "", "env": "",
                   "free": "ilimitado (tu hardware)"},
}

# Orden de preferencia para el combo (calidad ES + cuota + velocidad).
BACKEND_ORDER = ["gemini", "groq", "tokenharbor", "freellmapi", "cloudflare",
                 "nvidia", "deepseek", "cerebras", "openrouter", "mistral",
                 "cohere", "ollama"]

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
    "nvidia": "https://integrate.api.nvidia.com/v1",   # API catalog / NIM
}

# Cloudflare Workers AI: la base incluye la cuenta (no es secreto) porque
# el endpoint OpenAI-compatible es por cuenta.
CLOUDFLARE_ACCOUNT = "94e1b02f1e5564b54381b01e2d0a93f3"
OPENAI_BASES["cloudflare"] = (
    f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT}"
    "/ai/v1")

# Backends en los que SOLO se muestran/generan ids con este sufijo:
# lo demás del catálogo es de pago y no queremos gastar saldo.
# (Catálogos verificados en vivo el 2026-10-03.)
FREE_ONLY = {"tokenharbor": ":free", "openrouter": ":free"}

# Alias que no terminan en el sufijo pero también son gratis y hay que
# conservar en la cadena (el meta-router de OpenRouter).
FREE_KEEP = {"openrouter": {"openrouter/free"}}

# Ids del catálogo que NO sirven para chat/guiones (tareas que no son
# texto: embeddings, imágenes, audio, filtros de seguridad…).
FREE_EXCLUDE = {"cloudflare": ("embed", "image", "diffusion", "flux",
                               "whisper", "tts", "audio", "rerank",
                               "transcri", "resnet", "distilbert", "guard",
                               "smart-turn", "clef", "m2m", "indictrans",
                               "detection", "classif", "bge",
                               "sentence-transformers",
                               # voz/vision: no son chat (2026-10-08)
                               "deepgram", "llava"),
                # Gemini: tts, imagen y los pro retirados (404).
                "gemini": ("tts", "image", "banana", "2.5-pro", "video"),
                # Groq: audio, clasificadores de seguridad y los orpheus
                # que exigen aceptar términos. llama-3.3-70b-versatile
                # ya no existe (404 verificado el 2026-10-08).
                "groq": ("whisper", "guard", "safeguard", "orpheus",
                         "llama-3.3-70b-versatile"),
                # Mistral: completado intermedio (fim), CLI de vibe y
                # modelos Labs (403: requieren admin).
                "mistral": ("fim", "vibe-cli", "labs"),
                # NVIDIA API catalog: 80 ids, muchos no son de chat.
                "nvidia": ("embed", "vision", "guard", "safety", "reward",
                           "parse", "detector", "clip", "deplot", "diffusion",
                           "cosmos", "neva", "vila", "translate", "chatqa",
                           "starcoder", "codellama", "codegemma", "coder",
                           "codestral", "code-instruct")}

# Workers AI: estos ids existen en el catálogo pero NO corren en el plan
# Free (verificado en vivo el 2026-10-04 con la key real).
CF_FREE_BLOCKED = {
    "@cf/zai-org/glm-5.3", "@cf/zai-org/glm-5.3-flash", "@cf/zai-org/glm-5.2",
    "@cf/moonshotai/kimi-k2.6", "@cf/moonshotai/kimi-k2.7-code",
    "@cf/deepseek-ai/deepseek-v4-flash-0731",
    "@cf/deepseek-ai/deepseek-v4-pro-0813",
    "@cf/swiss-ai/apertus-v1.5-8b", "@cf/utter-project/eurollm-9b-it",
    "@cf/meta/llama-3.2-11b-vision-instruct",   # exige licencia (agree)
}

# NVIDIA API catalog: estos ids aparecen en GET /models pero la cuenta
# responde 404 "Function ... Not found for account" (verificado en vivo
# el 2026-10-05), así que no entran en la cadena.
NV_FREE_BLOCKED = {
    "01-ai/yi-large", "adept/fuyu-8b",
    "ai21labs/jamba-1.5-large-instruct", "aisingapore/sea-lion-7b-instruct",
    "databricks/dbrx-instruct", "google/gemma-2b", "google/gemma-3-12b-it",
    "google/gemma-3-4b-it", "google/recurrentgemma-2b",
    "ibm/granite-3.0-3b-a800m-instruct", "ibm/granite-3.0-8b-instruct",
    "meta/llama2-70b", "microsoft/kosmos-2", "microsoft/phi-3.5-moe-instruct",
    "mistralai/mistral-7b-instruct-v0.3", "mistralai/mistral-large",
    "mistralai/mistral-large-2-instruct", "mistralai/mixtral-8x22b-v0.1",
    "moonshotai/kimi-k2.6", "nv-mistralai/mistral-nemo-12b-instruct",
    "nvidia/llama-3.1-nemotron-51b-instruct",
    "nvidia/llama-3.1-nemotron-70b-instruct",
    "nvidia/llama-3.1-nemotron-ultra-253b-v1",
    "nvidia/mistral-nemo-minitron-8b-8k-instruct",
    "nvidia/nemotron-4-340b-instruct", "nvidia/nemotron-nano-3-30b-a3b",
    "writer/palmyra-creative-122b", "writer/palmyra-fin-70b-32k",
    "writer/palmyra-med-70b", "writer/palmyra-med-70b-32k",
    "zyphra/zamba2-7b-instruct",
    # Responden con timeout (probado con 45/60/180 s): no sirven.
    "deepseek-ai/deepseek-v4.1-flash", "google/gemma-4-31b-it",
    "z-ai/glm-5.3-flash",
}

# Alias del router FreeLLMAPI: `auto` deja que su router elija el mejor
# modelo gratis disponible (auto:smart/auto:fast/auto:cheap = prioridades);
# `fusion` prueba varios a la vez (lento, pero no se queda sin ruta).
ROUTER_ALIASES = {"freellmapi": ["auto", "auto:smart", "auto:fast",
                                 "auto:cheap", "fusion"]}

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
    # 2026-10-08: los flash dan 429 (cuota diaria agotada); los lite y
    # gemma responden. Orden: lo que responde HOY primero.
    "gemini": ["gemini-2.5-flash-lite", "gemini-flash-lite-latest",
               "gemini-3-flash-preview", "gemini-3.5-flash-lite",
               "gemini-3.1-flash-lite", "gemini-flash-latest",
               "gemini-3.8-flash", "gemini-3.5-flash", "gemini-2.5-flash",
               "gemma-4-26b-a4b-it"],
    # 2026-10-08: llama-3.3-70b-versatile → 404; el resto OK.
    "groq": ["openai/gpt-oss-120b", "openai/gpt-oss-20b",
             "qwen/qwen3.8-27b", "allam-2-7b"],
    "cerebras": ["zai-glm-4.7", "gpt-oss-120b", "llama-3.3-70b"],
    # La key responde 401 «User not found» (regenerarla); ids alineados
    # con el catálogo :free descubierto el 2026-10-08.
    "openrouter": [
        "nvidia/nemotron-3-super-120b-a12b:free",
        "nvidia/nemotron-3-ultra-550b-a55b:free",
        "nvidia/nemotron-3.5-lightning:free",
        "google/gemma-4-31b-it:free",
        "thinkingmachines/inkling:free",
        "poolside/laguna-xs-2.1:free",
        "openrouter/free",  # meta-router: elige un :free disponible
    ],
    # 2026-10-08: small/medium/magistral en 429; ministral responde.
    "mistral": ["ministral-14b-latest", "mistral-small-latest",
                "mistral-medium-latest", "magistral-small-latest",
                "codestral-latest"],
    "cohere": ["command-a-03-2025", "command-r-plus", "command-r"],
    # Solo ids gratuitos: con la key, resolve_chain() los sustituye por
    # los que devuelva /models filtrando el mismo sufijo.
    # 2026-10-08: qwen3.8-flash:free terminó (404); entra claude-haiku
    # (la bolsa de 7 días está agotada: 429 hasta que se renueve).
    "tokenharbor": ["mimo-v2.6-flash:free", "deepseek-v4.1-flash:free",
                    "deepseek-v4-flash:free", "mimo-v2.5:free",
                    "claude-haiku-5.5:free"],
    # 2026-10-08: gemini-2.5-flash ya no existe upstream (404);
    # agnes-2.5-flash y deepseek-v4-flash responden hoy.
    "freellmapi": ["deepseek-v4-flash", "agnes-2.5-flash", "glm-4.7",
                   "kimi-k3", "glm-5.3", "qwen3.8-flash"],
    # Workers AI: ids verificados en vivo el 2026-10-04/08 en plan Free,
    # de mejor a peor para español (los 12 respondieron).
    "cloudflare": ["@cf/meta/llama-3.3-70b-instruct-fp8-fast",
                   "@cf/qwen/qwen3.8-27b", "@cf/openai/gpt-oss-120b",
                   "@cf/mistralai/mistral-small-3.1-24b-instruct",
                   "@cf/qwen/qwen3-30b-a3b-fp8",
                   "@cf/aisingapore/gemma-sea-lion-v4-27b-it",
                   "@cf/google/gemma-4-26b-a4b-it",
                   "@cf/nvidia/nemotron-3-120b-a12b",
                   "@cf/zai-org/glm-4.7-flash",
                   "@cf/deepseek-ai/deepseek-r1-distill-qwen-32b",
                   "@cf/meta/llama-4-scout-17b-16e-instruct",
                   "@cf/qwen/qwq-32b"],
    # NVIDIA API catalog: de los 80 ids del catálogo solo 10 responden en
    # esta cuenta (verificado en vivo el 2026-10-05), ordenados por
    # velocidad/calidad para español.
    "nvidia": ["nvidia/nemotron-3-super-120b-a12b",
               "z-ai/glm-5.3", "openai/gpt-oss-20b",
               "nvidia/nemotron-3.5-lightning-30b-a3b",
               "nvidia/nemotron-3-ultra-550b-a55b",
               "moonshotai/kimi-k3",
               "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
               "meta/muse-glimmer-30b"],
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
    _set_usage("ollama", model, out,
               (system or "") + "\n" + (prompt or ""),
               (out.get("response") or ""))
    text = (out.get("response") or "").strip()
    if not text and out.get("thinking"):
        raise LLMError("El modelo local solo devolvió razonamiento "
                       "(vacío). Elige otro modelo o ponlo en modo no "
                       "pensante.")
    return text


# Último consumo reportado por el backend (lo llena cada _xxx_generate).
# Lo lee el panel para el Medidor de tokens. None si el backend no lo reporta.
LAST_USAGE = None


def _set_usage(backend, model, out, prompt="", response=""):
    """Extrae {prompt_tokens, completion_tokens} del JSON crudo (best-effort).

    OpenAI-compatibles (groq/deepseek/openrouter/cerebras/mistral/...):
    out["usage"]. Gemini: out["usageMetadata"]. Ollama: prompt_eval_count.
    Si el backend no reporta uso, se ESTIMA por longitud (≈4 chars/token)
    y se marca estimado=True para que el Medidor lo indique con ~.
    """
    global LAST_USAGE
    pt = ct = None
    estimado = False
    try:
        o = out or {}
        u = o.get("usage") or {}
        pt, ct = u.get("prompt_tokens"), u.get("completion_tokens")
        if pt is None:
            um = o.get("usageMetadata") or {}
            pt, ct = um.get("promptTokenCount"), um.get("candidatesTokenCount")
        if pt is None and "prompt_eval_count" in o:
            pt, ct = o.get("prompt_eval_count"), o.get("eval_count")
    except Exception:
        pt = ct = None
    if pt is None:
        pt = max(1, len(prompt or "") // 4)
        ct = max(1, len(response or "") // 4)
        estimado = True
    LAST_USAGE = {"backend": backend, "model": model,
                  "prompt_tokens": pt, "completion_tokens": ct,
                  "estimado": estimado}


# Límite de salida por minuto (OTPM) de Groq: pedir más de 1.000 tokens
# de golpe devuelve 400 aunque el modelo lo necesite. El resto de backends
# usan el máximo por defecto.
MAX_TOKENS = {"groq": 1000}  # OTPM 1000: 1200 rompe qwen3.8-27b (400); 1024 y 512 van bien

# Timeout por backend (segundos). NVIDIA deja colgados los endpoints que no
# están provisionados para la cuenta: mejor cortar pronto y pasar al
# siguiente modelo de la cadena (los buenos responden en <60 s).
CHAT_TIMEOUT = {"nvidia": 120}


def _rate_kind(msg):
    """Clasifica un error: 'blocked' (bloqueo de red/región: no reintentar
    ni seguir con este backend), 'wait' (se libera solo, reintentar),
    'skip' (cuota diaria/facturación: saltar al siguiente modelo),
    None (no es cuota)."""
    m = (msg or "").lower()
    if "too large for model" in m:
        return None   # error duro de cuota: reintentar no arregla nada
    # Groq responde 403 "Access denied. Please check your network
    # settings." cuando bloquea la IP/país (p. ej. con VPN): reintentar
    # no sirve, hay que rotar de backend.
    if any(p in m for p in ("access denied", "check your network",
                            "not available in your region",
                            "unsupported country", "country not supported")):
        return "blocked"
    skip = ("exceeded your current quota", "quota exceeded",
            "daily quota", "tokens per day", "tpd",
            "check your plan", "billing",
            "resource_exhausted", "insufficient_quota", "insufficient funds",
            "account", "suspend",
            # Workers AI (plan Free): modelo no disponible / sin licencia.
            "free plan", "does not have config", "must submit the prompt",
            # NVIDIA: modelos retirados del catálogo (HTTP 410 Gone).
            "end of life",
            # 403 genérico de un modelo concreto: saltar, no abortar.
            "http 403", "forbidden")
    if any(p in m for p in skip):
        return "skip"
    wait = ("rate limit", "too many requests", " 429",
            "output tokens per minute", "requests per minute",
            "tokens per minute", "try again", "temporarily",
            "overloaded", "server busy",
            # Cortes de conexión transitorios (el servidor mata la petición
            # a la mitad): reintentar sí sirve, no es cuota.
            "remote end closed", "connection reset", "connection aborted",
            "timed out", "timeout", "temporary failure",
            # NVIDIA: workers saturados o aún desplegando el endpoint.
            "service unavailable", " 503", "request limit reached",
            "resourceexhausted")
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
                 max_tokens=8192, backend="openai"):
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
        timeout=CHAT_TIMEOUT.get(backend, 300),
    )
    try:
        _resp_oa = out["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise LLMError(f"Respuesta inesperada de {model}: {str(out)[:200]}")
    # content puede venir null (modelo saturado, filtro de contenido o
    # corte por max_tokens): no es AttributeError, es "vacía" para que la
    # cadena avance al siguiente modelo en vez de matar la etapa.
    if not _resp_oa or not _resp_oa.strip():
        raise LLMError(f"El modelo {model} devolvió contenido vacío "
                       f"(content=null).")
    _resp_oa = _resp_oa.strip()
    _set_usage(backend, model, out,
               (system or "") + "\n" + (prompt or ""), _resp_oa)
    return _resp_oa


def _openai_models(base, api_key):
    """Descubre modelos vía GET {base}/models. [] si falla."""
    try:
        out = _get_json(f"{base}/models",
                        headers={"Authorization": f"Bearer {api_key}"})
        return [m["id"] for m in out.get("data", []) if m.get("id")]
    except LLMError:
        return []


def _cloudflare_models(api_key):
    """Workers AI: el catálogo sale de /ai/models/search (GET /models da
    405 en el endpoint OpenAI-compatible). Devuelve los `name` (@cf/…)."""
    try:
        out = _get_json(
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{CLOUDFLARE_ACCOUNT}/ai/models/search",
            headers={"Authorization": f"Bearer {api_key}"})
        return [m["name"] for m in out.get("result", []) if m.get("name")]
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
    _set_usage("openrouter", model, out,
               (system or "") + "\n" + (prompt or ""),
               ((out.get("choices") or [{}])[0].get("message", {}).get("content") or ""))
    try:
        _resp_or = out["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise LLMError(f"Respuesta inesperada de {model}: {str(out)[:200]}")
    # content null (saturación/filtro/corte): LLMError para que la cadena
    # avance al siguiente modelo en vez de matar la etapa con AttributeError.
    if not _resp_or or not _resp_or.strip():
        raise LLMError(f"El modelo {model} devolvió contenido vacío "
                       f"(content=null).")
    return _resp_or.strip()


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
    _parts_gem = []
    try:
        _parts_gem = out["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError, TypeError):
        pass
    _set_usage("gemini", model, out, (system or "") + "\n" + (prompt or ""),
               "".join(p.get("text", "") for p in _parts_gem))
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
    _set_usage("cohere", model, out, (system or "") + "\n" + (prompt or ""),
               out.get("text") or "")
    text = out.get("text")
    if not text:
        raise LLMError(f"Respuesta inesperada de {model}: {str(out)[:200]}")
    return text.strip()


# ---------- resolución de cadena ----------
def _descubierto(backend, keys):
    """Ids que devuelve el catálogo del backend, YA filtrados (solo chat
    y gratuitos). `[]` si no hay key o el descubrimiento falla."""
    key = (keys or {}).get(backend, "")
    if not key:
        return []
    try:
        if backend == "gemini":
            found = _gemini_models(key)
        elif backend == "cloudflare":
            found = _cloudflare_models(key)
        elif backend == "openrouter":
            found = _openai_models(OPENROUTER_URL.rsplit("/chat", 1)[0], key)
        elif backend in OPENAI_BASES:
            found = _openai_models(_base(backend, keys), key)
        else:
            return []
    except Exception:
        return []
    if not found:
        return []
    if backend == "cloudflare":
        bad = FREE_EXCLUDE["cloudflare"]
        return [m for m in found
                if m not in CF_FREE_BLOCKED
                and not any(t in m.lower() for t in bad)]
    if backend == "nvidia":
        bad = FREE_EXCLUDE["nvidia"]
        return [m for m in found
                if m not in NV_FREE_BLOCKED
                and not any(t in m.lower() for t in bad)]
    if backend in FREE_EXCLUDE:  # quitar ids que no son de chat
        bad = FREE_EXCLUDE[backend]
        found = [m for m in found
                 if not any(t in m.lower() for t in bad)]
    if backend in FREE_ONLY:  # solo ids gratuitos (p.ej. `:free`)
        suf = FREE_ONLY[backend]
        keep = FREE_KEEP.get(backend, set())
        found = [m for m in found if m.endswith(suf) or m in keep]
    return found


def resolve_chain(backend, model, keys):
    """Modelos a intentar, en orden. `model` explícito va primero y solo."""
    if model:
        return [model]
    found = _descubierto(backend, keys)
    pref = list(PREFERRED.get(backend, []))
    if not found:
        return list(ROUTER_ALIASES.get(backend, [])) + pref
    ok = [m for m in pref if m in found]
    rest = [m for m in found if m not in ok]
    if backend in MODEL_CAP:  # catálogo enorme: alias + tope
        alias = list(ROUTER_ALIASES.get(backend, ()))
        rest = rest[:max(0, MODEL_CAP[backend] - len(alias) - len(ok))]
        return alias + ok + rest
    return ok + rest[:2]


def generate(prompt, backend="gemini", model="", system="", keys=None,
             api_key=""):
    """Genera texto. Devuelve (texto, modelo_usado).

    keys: dict {"gemini": "...", "groq": "...", ...}. `api_key` es el
    legado de openrouter (se respeta si keys no lo trae).
    Recorre la cadena del backend hasta que un modelo responda. Si el
    backend elegido cae entero (bloqueo de red, cuota, ids retirados),
    rota a los demás backends gratuitos con key antes de rendirse.
    """
    global LAST_USAGE
    LAST_USAGE = None  # cada llamada reporta su propio consumo
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
            f"'{BACKENDS[backend]['label']}'. Ponla en Configuraci\u00f3n.")

    def _call(b, m):
        k = keys.get(b, "")
        if b == "gemini":
            return _gemini_generate(k, m, prompt, system)
        if b == "cohere":
            return _cohere_chat(k, m, prompt, system)
        if b == "openrouter":
            return _openrouter_generate(m, prompt, system, k)
        # groq, cerebras, mistral, tokenharbor, freellmapi, cloudflare,
        # deepseek, nvidia
        return _openai_chat(_base(b, keys), k, m, prompt, system,
                            max_tokens=MAX_TOKENS.get(b, 8192), backend=b)

    errors = []
    estado = {"bloqueado": False}

    def _intentar(chain):
        """Prueba una cadena entera; devuelve (texto, modelo) o None."""
        for m in chain:
            if estado["bloqueado"]:
                return None
            for attempt in range(3):  # 3 intentos si pide esperar
                try:
                    text = _call(backend, m)
                    if not text:
                        raise LLMError("respuesta vac\u00eda")
                    return text, m
                except LLMError as e:
                    kind = _rate_kind(str(e))
                    if kind == "blocked":
                        estado["bloqueado"] = True
                        errors.append(f"{m}: bloqueo de red/regi\u00f3n ({e})")
                        return None
                    if kind == "wait" and attempt < 2:
                        time.sleep(_rate_wait(str(e)))  # se libera sola
                        continue
                    if kind == "skip":
                        errors.append(f"{m}: cuota agotada, salto al siguiente "
                                      f"modelo ({e})")
                        break          # no tiene caso reintentar el mismo
                    errors.append(f"{m}: {e}")
                    break
        return None

    res = _intentar(resolve_chain(backend, model, keys))
    if res:
        return res
    # Modelo fijo que no respondió: antes de rendirse, prueba el resto
    # de modelos del MISMO backend (elige otro y sigue funcionando).
    if model and not estado["bloqueado"]:
        resto = [m for m in resolve_chain(backend, "", keys) if m != model]
        res = _intentar(resto)
        if res:
            return res

    # Rotaci\u00f3n autom\u00e1tica: si el backend elegido no respondi\u00f3,
    # probamos los dem\u00e1s gratuitos con key (nunca DeepSeek, que es de
    # pago, ni Ollama, que necesita su modelo en el combo).
    for b in BACKEND_ORDER:
        if b == backend or b in ("deepseek", "ollama") or not keys.get(b):
            continue
        for m in resolve_chain(b, "", keys)[:3]:
            try:
                text = _call(b, m)
                if text:
                    return text, f"{m} \u00b7 {b}"
            except LLMError as e:
                errors.append(f"[rotado a {b}] {m}: {e}")
                continue

    detalle = "\n".join(errors[:10])
    raise LLMError(f"Ning\u00fan modelo de '{backend}' respondi\u00f3.\n" +
                   detalle +
                   "\nQu\u00e9 probar: 1) espera 2-3 min (cuota por minuto); "
                   "2) cambia de backend en el panel (Gemini/Cloudflare/"
                   "Mistral suelen responder); 3) revisa la key en "
                   "Configuraci\u00f3n.")


def backend_options():
    return list(BACKEND_ORDER)


def model_options(backend, keys=None):
    """Opciones para el combo: preferidos primero y DESPUÉS todo lo que
    devuelva el catálogo (ya filtrado), para poder elegir cualquier
    modelo gratuito. Los preferidos que el catálogo no devuelve también
    se listan (pueden seguir siendo válidos)."""
    if backend == "ollama":
        # Fuera modelos de embeddings: no sirven para chat/guiones.
        return [m for m in list_ollama_models() if "embed" not in m.lower()]
    if backend not in BACKEND_ORDER:
        return []
    keys = keys or {}
    alias = list(ROUTER_ALIASES.get(backend, []))
    pref = list(PREFERRED.get(backend, []))
    found = _descubierto(backend, keys)
    if not found:
        return alias + pref
    ok = [m for m in pref if m in found]
    rest = [m for m in found if m not in ok]
    cap = MODEL_CAP.get(backend, 40)
    coger = max(0, cap - len(alias) - len(ok))
    return alias + ok + rest[:coger] + [m for m in pref if m not in found]
