#!/usr/bin/env python3
"""Orquestador del pipeline Zenn Factory (facade, v30).

Agrupa los modulos pipe_* y expone la API completa que app.py y los tests
importan como `pipeline.<nombre>`: execute_stage, run_all,
correr_etapa_garantizada, propose_topics y las utilidades.
"""
import json
import re
import sys
import time
from pathlib import Path

from pipe_core import (
    HERE, BASE, PANEL_VERSION,
    STAGES_LARGO, STAGES_RECORTE, STAGES_SHORT, GATES, MANUAL_STAGES,
    STAGE_HINTS, stages_for, stage_label,
    run, count_words, estimate_minutes, pget, job_dir_of, find_script,
    prompt_maestro, DEFAULT_PROMPT_MAESTRO, MIN_PALABRAS_GUION,
    fmt_eta, Progreso, _SENT_SPLIT,
    _narracion_guion, _probe_duration, _guardar_log, _es_fallo_quota, _NO_LLM,
    _audio_path,
)
from pipe_guion import (
    DOI_RE, PMID_RE, extract_references, run_investigacion, draft_script,
    expandir_guion, critic_review, run_guion_draft,
)
from pipe_storyboard import (
    STORYBOARD_PROMPT, PAQUETE_PROMPT,
    run_storyboard, run_continuar_storyboard, run_paquete, _scene_marks,
    _campo, _partir_guion, _renumerar_desde, _parse_storyboard, _narracion_job,
    _voz_words, _normalizar_campos, _escenas_validas, _quitar_repetidas,
    _limpiar_parte, _ultima_voz, _bloques_escena, _valor_campo_linea,
    _limpia_valor, _buscar_en_guion, _prompt_parte, _temas_cubiertos,
)
from pipe_tts import (
    run_tts, build_vo_json, run_tts_stage,
    cut_vertical, fmt_mmss, segmento_de_escena, sugerencia_corto,
    _ids_con_archivo, _bloque_crudo,
)
from pipe_anim import (
    RIG_API, SCENE_PROMPT, FIX_PROMPT,
    run_animacion, run_reanimar_escena, run_ensamblado,
    _generar_y_renderizar_escena, _validar_escena, _rig_source, _rig_api_text,
    _srt_time, _wrap_card, _build_srt, _strip_fences, _eval_vec,
    _kw, _num, _nombre_llamada, _texto_de, _cajas_texto, _cajas_prota,
    _checar_solape_texto, _checar_banda_vs_prota, _BANDAS, _MANIM_VEC,
    _TEXTO_POS, _TXT_DEF,
)
from pipe_verify import (
    verificar_elementos, reparar_faltantes, validar_etapa,
    _cobertura_storyboard, _repeticiones, _doble_final,
    _citas_sueltas, _auto_reparar, CONTRATO_ETAPAS, _PRE_ETAPA,
)
from pipe_thumbs import (
    THUMB_PROPS, _THUMB_EXPRS, _THUMB_PLAYERAS, _EXPR_KEYWORDS,
    thumbnail_concepts, thumbs_dir, run_thumbnails, run_miniatura,
    _fallback_expr, _fallback_concept, _short_text,
)

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
        except Exception as _e:
            # No interrumpe la etapa, pero el fallo deje rastro (Medidor).
            print(f"[medidor] no se registró uso de tokens: {_e}",
                  file=sys.stderr)
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

def correr_etapa_garantizada(p, stage, generate_fn=None, progress=None):
    """v28 — algoritmo de corrida garantizada para una etapa.

    1) PRE: valida los insumos (contratos de las etapas previas). Si un
       insumo está roto, no arranca: fallar aquí es mejor que un error
       críptico 3 etapas después.
    2) Ejecuta (execute_stage).
    3) POST: valida el contrato de salida.
    4) Si la etapa dijo "ok" pero el contrato no se cumple: UNA
       auto-reparación y reintento.
    5) Veredicto final honesto (nunca "ok" con productos rotos).

    Tiempos: no hay timeouts agresivos; cada etapa corre "con el tiempo
    necesario" (los subprocess usan sus propios límites generosos: TTS 3600s
    por lote, ffmpeg 900s por escena, HTTP 300s). Si un backend agota su
    cuota gratuita, llm.generate rota al siguiente ANTES de rendirse y la
    etapa continúa (no se trunca: la validación por partes + continuación
    automática aplica al texto venga del modelo que venga).
    Devuelve (ok, log, arts, sugg) como execute_stage.
    """
    job = job_dir_of(p)
    for pre in _PRE_ETAPA.get(stage, []):
        ok0, det0 = validar_etapa(pre, p, job)
        if not ok0:
            return (False,
                    f"⛔ Etapa '{stage}' no arranca: su insumo '{pre}' no "
                    f"cumple el contrato ({det0}). Completa '{pre}' primero; "
                    f"las etapas corren en orden.",
                    [], None)
    ok, log, arts, sugg = execute_stage(p, stage, generate_fn,
                                        progress=progress)
    vok, vdet = validar_etapa(stage, p, job)
    if ok and vok:
        return True, log + f"\n[contrato '{stage}': {vdet}]", arts, sugg
    if not ok:
        # La etapa ya falló fuerte con mensaje accionable: se respeta.
        return ok, log, arts, sugg
    # ok pero contrato roto: una auto-reparación y reintento.
    rep_txt = _auto_reparar(stage, p, job, generate_fn)
    ok2, log2, arts2, sugg2 = execute_stage(p, stage, generate_fn,
                                            progress=progress)
    vok2, vdet2 = validar_etapa(stage, p, job)
    if ok2 and vok2:
        return (True,
                log + f"\n[contrato '{stage}' incumplido ({vdet}); "
                f"auto-reparación: {rep_txt}; reintento validado: {vdet2}]",
                arts2, sugg2 or sugg)
    return (False,
            f"⛔ Etapa '{stage}': terminó pero su contrato no se cumple "
            f"({vdet}). Auto-reparación: {rep_txt}. Tras reintento: {vdet2}. "
            f"Log: {log[-600:]}",
            [], None)
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
    # Validación ANTES de correr: si una etapa está marcada "ok" pero le
    # faltan artefactos (p. ej. el storyboard creció después del TTS y S48
    # no tiene audio), se reabre para que se repare sola en vez de fallar
    # más adelante. El TTS omite los audios ya existentes: solo genera los
    # faltantes.
    try:
        job = job_dir_of(p)
        rep = verificar_elementos(p, job)["detalle"]
        if not rep["audios"]["ok"] or not rep["vo_json"]["ok"]:
            _db.set_stage(conn, pid, "tts", "pendiente",
                          "Verificación automática: faltan audios o vo.json "
                          "desactualizado; se regeneran solo los faltantes.")
    except Exception as _e:
        print(f"[run_all] pre-check de tts omitido: {_e}", file=sys.stderr)
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
        # v28: corrida garantizada — valida insumos, ejecuta, valida productos,
        # auto-repara una vez y da veredicto honesto (nunca "ok" con rotos).
        ok, log, arts, sugg = correr_etapa_garantizada(
            p, name, generate_fn, progress=on_progress)
        _db.set_stage(conn, pid, name,
                      sugg or ("ok" if ok else "fallo"), log, arts)
        if on_step:
            on_step(name, ok, log)
        if not ok:
            return "error", name
    return "done", ""
TOPIC_PROMPT = """Propón 8 temas para videos de curiosidad del canal "Indaga"
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


def propose_topics_youtube(youtube_key, niche, max_results=8):
    """Sugiere temas desde videos populares de YouTube (Data API v3).

    Busca videos largos relevantes del nicho y devuelve candidatos con el
    título como pregunta y vistas/canal como señal de interés. Devuelve
    (topics, error): error='' si todo fue bien. Requiere YOUTUBE_API_KEY
    de solo lectura (la subida usa OAuth aparte en youtube_upload).
    """
    import requests
    base = "https://www.googleapis.com/youtube/v3"
    try:
        r = requests.get(f"{base}/search", params={
            "part": "snippet", "q": niche, "type": "video",
            "videoDuration": "long", "order": "viewCount",
            "maxResults": min(max_results, 25), "relevanceLanguage": "es",
            "key": youtube_key,
        }, timeout=30)
        r.raise_for_status()
        items = r.json().get("items", [])
    except Exception as e:
        return [], f"Error de la API de YouTube: {e}"
    ids = [it["id"]["videoId"] for it in items
           if it.get("id", {}).get("videoId")]
    views = {}
    if ids:
        try:
            s = requests.get(f"{base}/videos", params={
                "part": "statistics", "id": ",".join(ids),
                "key": youtube_key,
            }, timeout=30)
            s.raise_for_status()
            for v in s.json().get("items", []):
                views[v["id"]] = int(
                    v.get("statistics", {}).get("viewCount", 0))
        except Exception:
            pass  # la señal de vistas es opcional: no bloquea
    topics = []
    for it in items:
        vid = it.get("id", {}).get("videoId")
        if not vid:
            continue
        sn = it.get("snippet", {})
        title = (sn.get("title") or "").strip()
        if not title:
            continue
        vc = views.get(vid)
        signal = (f"{vc:,} vistas · {sn.get('channelTitle', '')}" if vc
                  else sn.get("channelTitle", ""))
        topics.append({
            "question": title,
            "angle": (sn.get("description") or "")[:140].strip(),
            "signals": signal,
            "source": "youtube",
        })
        if len(topics) >= max_results:
            break
    return topics, ""
