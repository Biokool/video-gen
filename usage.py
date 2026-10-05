#!/usr/bin/env python3
"""Medidor de tokens: registro y resumen del consumo de LLMs por proyecto.

Cada llamada a un backend (vía execute_stage) se registra en
BASE/usage.jsonl, una línea JSON por llamada:
  {ts, pid, title, stage, backend, model, prompt_tokens, completion_tokens}

Los precios son de REFERENCIA (USD por millón de tokens) y editables en el
panel (vista Medidor). Los tiers gratuitos cuestan 0.
"""
import json
import time
from pathlib import Path

# Precios de referencia USD / 1M tokens (in, out). Aproximados: revísalos.
# Gratis = 0.0.
DEFAULT_PRICES = {
    # DeepSeek oficial (tarifa por token, según tu sidebar)
    "deepseek-chat": (0.27, 1.10),
    "deepseek-reasoner": (0.55, 2.19),
    # Groq (pago; el tier gratuito = 0)
    "llama-3.3-70b-versatile": (0.59, 0.79),
    "openai/gpt-oss-120b": (0.0, 0.0),
    "openai/gpt-oss-20b": (0.0, 0.0),
    # OpenRouter :free
    "nemotron-3-super-120b:free": (0.0, 0.0),
    "gemma-4-31b-it:free": (0.0, 0.0),
    "llama-3.3-70b-instruct:free": (0.0, 0.0),
    # Gemini
    "gemini-2.5-flash": (0.30, 2.50),
    "gemini-2.0-flash": (0.10, 0.40),
    # Ollama local
    "ollama": (0.0, 0.0),
}


def usage_file(base):
    return Path(base) / "usage.jsonl"


def record(base, pid, title, stage, backend, model, prompt_tokens,
           completion_tokens):
    """Agrega una línea al registro. Nunca falla (el medidor no rompe nada)."""
    try:
        rec = {"ts": time.time(), "pid": pid, "title": title, "stage": stage,
               "backend": backend or "", "model": model or "",
               "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens}
        with open(usage_file(base), "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


def read_all(base):
    recs = []
    fp = usage_file(base)
    if not fp.exists():
        return recs
    for line in fp.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            recs.append(json.loads(line))
        except Exception:
            continue
    return recs


def _model_key(r):
    return r.get("model") or r.get("backend") or "?"


def summarize(recs, prices=None):
    """Agrega por modelo y por proyecto. Devuelve dict listo para graficar."""
    prices = prices or {}
    por_modelo, por_proyecto = {}, {}
    total_in = total_out = llamadas = 0
    costo = 0.0
    for r in recs:
        mk = _model_key(r)
        pi = r.get("prompt_tokens") or 0
        po = r.get("completion_tokens") or 0
        llamadas += 1
        total_in += pi
        total_out += po
        m = por_modelo.setdefault(mk, {"llamadas": 0, "in": 0, "out": 0,
                                       "costo": 0.0})
        m["llamadas"] += 1
        m["in"] += pi
        m["out"] += po
        pin, pout = prices.get(mk, prices.get("__default__", (0.0, 0.0)))
        c = pi / 1e6 * pin + po / 1e6 * pout
        m["costo"] += c
        costo += c
        pk = str(r.get("pid", "?"))
        p = por_proyecto.setdefault(
            pk, {"title": r.get("title", ""), "llamadas": 0, "in": 0,
                 "out": 0, "costo": 0.0, "modelos": {}})
        p["llamadas"] += 1
        p["in"] += pi
        p["out"] += po
        p["costo"] += c
        pm = p["modelos"].setdefault(mk, 0)
        p["modelos"][mk] = pm + pi + po
    for m in por_modelo.values():
        m["total"] = m["in"] + m["out"]
    for p in por_proyecto.values():
        p["total"] = p["in"] + p["out"]
    return {"llamadas": llamadas, "in": total_in, "out": total_out,
            "total": total_in + total_out, "costo": costo,
            "por_modelo": por_modelo, "por_proyecto": por_proyecto}


def fmt_tokens(n):
    n = int(n or 0)
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)
