#!/usr/bin/env python3
"""Panel Zenn Factory — tablero visual del pipeline de videos.

Uso:
    pip install -r requirements.txt
    python3 seed.py        # solo la primera vez
    streamlit run app.py  # abre http://localhost:8501

Flujo: Bandeja (aprobar tema) → Proyectos → "Correr todo" avanza solo
y se detiene cuando necesita tu decisión (aprobar guion o miniatura)
o una etapa manual (animación, ensamblado).
"""
import sys
import time
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
import db
import llm
import pipeline
from pipeline import (BASE, stages_for, count_words, estimate_minutes,
                      propose_topics, draft_script, critic_review,
                      cut_vertical, execute_stage, run_all, stage_label,
                      STAGE_HINTS)

st.set_page_config(page_title="Zenn Factory · El Porqué", layout="wide")

conn = db.connect()
db.init_db()

# ---------- helpers ----------
def rerun():
    st.rerun()


def get(k, d=""):
    return db.get_setting(conn, k, d)


def project_kind_label(kind):
    return {"largo": "Largo 8–12 min",
            "corto-recorte": "Corto · recorte",
            "corto-standalone": "Corto · standalone"}.get(kind, kind)


def stage_badge(status):
    return {"pendiente": "⚪", "en-curso": "🟡",
            "ok": "🟢", "fallo": "🔴", "omitido": "⚫",
            "manual": "✅"}.get(status, "❔")


def fmt_dur(secs):
    secs = int(round(secs))
    if secs < 60:
        return f"{secs}s"
    m, s = divmod(secs, 60)
    return f"{m}m{s:02d}s"


def duracion_de(log):
    """Extrae '⏱ Duración: Xm' del log de una etapa, si existe."""
    import re
    m = re.search(r"⏱ Duración: (\S+)", log or "")
    return m.group(1) if m else ""


def apply_stage_result(pid, stage, ok, log, arts, sugg):
    db.set_stage(conn, pid, stage, sugg or ("ok" if ok else "fallo"),
                 log, arts)


def ejecutar_con_progreso(pid, p, stage, gen_fn, titulo):
    """Ejecuta UNA etapa con indicador visible, barra de progreso y ETA.

    Muestra un panel st.status con la barra mientras corre, guarda la
    duración en el log y marca la etapa. Devuelve (ok, log).
    """
    st.session_state["running"] = (pid, titulo)
    box = st.status(f"▶ {titulo} — en ejecución…", expanded=True)
    bar = box.progress(0, text="Iniciando…")

    def cb(_skey, done, total, det):
        bar.progress(min(done / max(total, 1), 1.0), text=det)

    t0 = time.time()
    try:
        ok, log, arts, sugg = execute_stage(p, stage, gen_fn,
                                            progress=cb)
    finally:
        st.session_state.pop("running", None)
    dt = time.time() - t0
    log = (log or "") + f"\n⏱ Duración: {fmt_dur(dt)}"
    apply_stage_result(pid, stage, ok, log, arts, sugg)
    box.update(label=f"{'✅' if ok else '❌'} {titulo} — {fmt_dur(dt)}",
               state="complete" if ok else "error", expanded=not ok)
    return ok, log


def all_keys():
    keys = {b: get(llm.BACKENDS[b]["setting"])
            for b in llm.BACKENDS if llm.BACKENDS[b]["setting"]}
    keys["freellmapi_base"] = get("freellmapi_base", llm.FREELLMAPI_BASE)
    return keys


def make_generate_fn(backend, model):
    keys = all_keys()
    def fn(prompt, system=""):
        return llm.generate(prompt, backend=backend, model=model,
                            system=system, keys=keys)
    fn.backend = backend  # el pipeline lo usa para pacing (Groq OTPM)
    return fn


# ---------- sidebar: modelo (combo) ----------
st.sidebar.title("🎛️ Modelo")
bopts = llm.backend_options()
saved_backend = get("backend", "openrouter")
backend = st.sidebar.selectbox(
    "Backend", bopts,
    index=bopts.index(saved_backend) if saved_backend in bopts else 0,
    format_func=lambda b: llm.BACKENDS[b]["label"],
    key="backend")
bmeta = llm.BACKENDS[backend]
if bmeta["setting"] and not get(bmeta["setting"]):
    st.sidebar.warning(f"Sin {bmeta['env']} — ponla en Configuración "
                       "o elige Ollama local.")
else:
    st.sidebar.caption(f"Gratis: {bmeta['free']}")
models = llm.model_options(backend, all_keys())
if backend == "ollama" and not models:
    st.sidebar.warning("Ollama no responde en localhost:11434. Revisa `ollama serve`.")
default_model = get("default_model_id", "")
idx = models.index(default_model) if default_model in models else 0
model_id = st.sidebar.selectbox("Modelo", models or ["(sin modelos)"],
                                index=idx if models else 0)
if st.sidebar.button("Guardar como predeterminado"):
    db.set_setting(conn, "backend", backend)
    db.set_setting(conn, "default_model_id", model_id)
    st.sidebar.success("Guardado.")

st.sidebar.divider()
# ---- indicador global: algo se está ejecutando ----
_running = st.session_state.get("running")
if _running:
    st.sidebar.error(f"▶ CORRIENDO\n\n{_running[1]}\n(proyecto #{_running[0]})")
    st.sidebar.caption("No pulses otros botones hasta que termine.")
view = st.sidebar.radio("Vista", ["📥 Bandeja de temas", "🎬 Proyectos",
                                  "⚙️ Configuración"])
st.sidebar.divider()
st.sidebar.caption("Panel v7 · Zenn Factory")

gen_fn = make_generate_fn(backend, model_id)


def apply_stage_result(pid, stage, ok, log, arts, sugg):
    db.set_stage(conn, pid, stage, sugg or ("ok" if ok else "fallo"),
                 log, arts)


# ============================================================ BANDEJA
if view == "📥 Bandeja de temas":
    st.title("📥 Bandeja de temas")
    st.caption("Paso 1 del flujo: aprueba un tema y se crea el proyecto. "
               "Después, en Proyectos, pulsa «Correr todo».")
    c1, c2 = st.columns([3, 1])
    with c1:
        with st.form("nuevo_tema"):
            q = st.text_input("Pregunta del video")
            angle = st.text_input("Ángulo (por qué engancha)")
            if st.form_submit_button("Añadir tema manual"):
                if q.strip():
                    db.add_topic(conn, q.strip(), angle.strip())
                    st.success("Tema añadido.")
                    rerun()
    with c2:
        st.write("Propuestas del sistema")
        if st.button("🤖 Generar 8 propuestas (LLM)"):
            try:
                with st.spinner("Generando..."):
                    topics = propose_topics(gen_fn)
                for t in topics:
                    db.add_topic(conn, t["question"], t["angle"],
                                 t["source"], t["signals"])
                st.success(f"{len(topics)} propuestas añadidas.")
                rerun()
            except Exception as e:
                st.error(str(e))
        yt = get("youtube_key")
        if st.button("📺 Sugerir desde YouTube"):
            if not yt:
                st.warning("Configura YOUTUBE_API_KEY en Configuración.")
            else:
                st.info("Conector YouTube: pendiente de implementar con tu key.")

    st.divider()
    filtro = st.selectbox("Estado", ["propuesto", "aprobado", "rechazado", "archivado"])
    for t in db.list_topics(conn, filtro):
        with st.expander(f"{t['question']}  ·  {t['source']}"):
            if t["angle"]:
                st.write(f"**Ángulo:** {t['angle']}")
            if t["signals"]:
                st.write(f"**Señal:** {t['signals']}")
            if t["notes"]:
                st.write(f"**Notas:** {t['notes']}")
            b1, b2, b3, b4 = st.columns(4)
            with b1:
                if st.button("✅ Aprobar", key=f"ap{t['id']}"):
                    kind = st.session_state.get(f"kind{t['id']}", "largo")
                    pid = db.add_project(
                        conn, t["question"], topic_id=t["id"], kind=kind,
                        model_backend=backend, model_id=model_id,
                        job_dir=f"jobs/{t['id']}")
                    db.ensure_stages(conn, pid, [s for s, _, _ in stages_for(kind)])
                    db.ensure_approvals(conn, pid)
                    db.set_approval(conn, pid, "tema", "aprobado")
                    db.set_stage(conn, pid, "tema", "ok",
                                 "Tema aprobado en la bandeja.")
                    db.set_topic_status(conn, t["id"], "aprobado")
                    st.success(f"Proyecto #{pid} creado ({kind}). "
                               "Ve a 🎬 Proyectos y pulsa «Correr todo».")
                    rerun()
            with b2:
                st.selectbox("Tipo", ["largo", "corto-recorte", "corto-standalone"],
                             key=f"kind{t['id']}", label_visibility="collapsed")
            with b3:
                if st.button("🗑 Rechazar", key=f"rj{t['id']}"):
                    db.set_topic_status(conn, t["id"], "rechazado")
                    rerun()
            with b4:
                if st.button("📦 Archivar", key=f"ar{t['id']}"):
                    db.set_topic_status(conn, t["id"], "archivado")
                    rerun()

# ============================================================ PROYECTOS
elif view == "🎬 Proyectos":
    if "project_id" not in st.session_state:
        st.title("🎬 Proyectos")
        projs = db.list_projects(conn)
        if not projs:
            st.info("Sin proyectos. Aprueba un tema en la bandeja.")
        for p in projs:
            done, total = db.stage_progress(conn, p["id"])
            cols = st.columns([5, 2, 2, 1])
            cols[0].write(f"**#{p['id']} {p['title']}**")
            cols[1].write(project_kind_label(p["kind"]))
            cols[2].progress(done / max(total, 1), text=f"{done}/{total} etapas")
            if cols[3].button("Abrir", key=f"op{p['id']}"):
                st.session_state["project_id"] = p["id"]
                rerun()
    else:
        pid = st.session_state["project_id"]
        p = db.get_project(conn, pid)
        if st.button("← Volver a proyectos"):
            del st.session_state["project_id"]
            rerun()
        st.title(f"#{p['id']} {p['title']}")
        import tts_engine as _te
        _veng, _vvoz = _te.parse_spec(p["voice"])
        _vlabel = dict(_te.VOICE_CATALOG.get(_veng, {}).get("voices", [])
                       ).get(_vvoz, p["voice"])
        st.caption(f"{project_kind_label(p['kind'])} · 🎙️ {_vlabel} · "
                   f"{p['language']} · modelo del sidebar: "
                   f"{llm.BACKENDS[backend]['label']} / {model_id}")

        stages = db.list_stages(conn, pid)
        total = len(stages)
        done_n, _ = db.stage_progress(conn, pid)
        st.progress(done_n / max(total, 1),
                    text=f"Progreso: {done_n}/{total} etapas")

        # ---- siguiente paso ----
        def next_step():
            for i, s in enumerate(stages):
                if s["status"] in ("ok", "manual", "omitido"):
                    continue
                name = s["stage"]
                if name == "guion" and s["status"] == "en-curso" and \
                        db.get_approval(conn, pid, "guion")["status"] != "aprobado":
                    return ("👉 **Siguiente paso:** el borrador del guion está "
                            "listo. Léelo y apruébalo en la **Puerta 1** (abajo).")
                if name == "miniatura" and s["status"] == "ok" and \
                        db.get_approval(conn, pid, "miniatura")["status"] != "aprobado":
                    return ("👉 **Siguiente paso:** elige una miniatura en la "
                            "**Puerta 2** (abajo) para poder cerrar el paquete.")
                hint = STAGE_HINTS.get(name, "")
                return (f"👉 **Siguiente paso:** etapa {i + 1}/{total} · "
                        f"**{stage_label(p['kind'], name)}**. {hint}")
            return "🎉 **Proyecto completo.** Todas las etapas están cerradas."

        st.info(next_step())

        # ---- correr todo ----
        if "run_msg" in st.session_state:
            kind_msg, txt = st.session_state.pop("run_msg")
            (st.success if kind_msg == "ok" else st.warning)(txt)
        if st.button("▶ Correr todo (avanza solo y se detiene si te necesita)",
                     type="primary", disabled=bool(_running)):
            st.session_state["running"] = (pid, "Correr todo")
            box = st.status("▶ Correr todo — en ejecución…", expanded=True)
            bar = box.progress(0, text="Iniciando…")
            lines = []
            n_pend = len([s for s in stages
                          if s["status"] not in ("ok", "manual", "omitido")])
            hecho = {"n": 0}

            def on_step(name, ok, log):
                hecho["n"] += 1
                lines.append(f"{'✅' if ok else '❌'} "
                             f"{stage_label(p['kind'], name)}")
                box.write("\n\n".join(lines))

            def cb(_skey, done, total, det):
                frac = (hecho["n"] + min(done / max(total, 1), 1.0))
                bar.progress(min(frac / max(n_pend, 1), 1.0),
                             text=f"Etapa {hecho['n'] + 1}/{n_pend} · {det}")

            try:
                reason, detail = run_all(conn, p, gen_fn, on_step=on_step,
                                         on_progress=cb)
            finally:
                st.session_state.pop("running", None)
            box.update(label="⏸ Correr todo — detenido (te necesita)" if reason != "done"
                       else "✅ Correr todo — completo",
                       state="complete", expanded=False)
            if reason == "done":
                msg = ("ok", "✅ Todo ejecutado. Revisa el paquete de publicación.")
            elif reason == "gate" and detail == "guion":
                msg = ("warn", "⏸ Detenido en la **Puerta 1 (guion)**: el borrador "
                               "está generado. Léelo abajo y pulsa «Aprobar guion».")
            elif reason == "gate" and detail == "miniatura":
                msg = ("warn", "⏸ Detenido en la **Puerta 2 (miniatura)**: elige "
                               "una miniatura abajo para cerrar el paquete.")
            elif reason == "manual":
                msg = ("warn", f"⏸ Detenido en etapa manual: "
                               f"**{stage_label(p['kind'], detail)}**. "
                               f"{STAGE_HINTS.get(detail, '')} "
                               "Cuando la termines, pulsa «Marcar hecho» en su etapa "
                               "y vuelve a «Correr todo».")
            elif reason == "error":
                msg = ("warn", f"❌ Falló la etapa **{stage_label(p['kind'], detail)}**. "
                               "Abre esa etapa para ver el error exacto.")
            else:
                msg = ("warn", f"Detenido: {reason} {detail}")
            st.session_state["run_msg"] = msg
            rerun()

        # ---- config rápida ----
        with st.expander("⚙️ Configuración del proyecto"):
            import tts_engine
            peng, pvoice = tts_engine.parse_spec(p["voice"])
            pengs = tts_engine.ENGINES
            ck1, ck2 = st.columns(2)
            sel_eng = ck1.selectbox(
                "Motor de voz", pengs,
                index=pengs.index(peng) if peng in pengs else 0,
                format_func=lambda e: tts_engine.VOICE_CATALOG[e]["label"],
                key=f"veng{pid}")
            vlist = tts_engine.VOICE_CATALOG[sel_eng]["voices"]
            vids = [v for v, _ in vlist]
            sel_voice = ck2.selectbox(
                "Voz", vids,
                index=vids.index(pvoice) if sel_eng == peng and pvoice in vids else 0,
                format_func=lambda v: dict(vlist)[v],
                key=f"vvoz{pid}")
            ck3, ck4 = st.columns(2)
            nl = ck3.text_input("Idioma", p["language"])
            nm = ck4.text_input("Modelo", p["model_id"])
            if st.button("Guardar config"):
                db.update_project(conn, pid, voice=f"{sel_eng}:{sel_voice}",
                                  language=nl, model_id=nm)
                st.success("Guardado.")
                rerun()

        # ---- tablero de etapas (numerado, en orden) ----
        st.subheader("Pipeline · se ejecuta en este orden")
        for i, s in enumerate(stages):
            sname = stage_label(p["kind"], s["stage"])
            auto = dict((x[0], x[2]) for x in stages_for(p["kind"])).get(s["stage"], "?")
            dur = duracion_de(s["log"])
            titulo = (f"**{i + 1}/{total}** {stage_badge(s['status'])} "
                      f"{sname} · `{auto}` · {s['status']}"
                      + (f" · ⏱ {dur}" if dur else ""))
            with st.expander(titulo):
                hint = STAGE_HINTS.get(s["stage"])
                if hint:
                    st.caption("💡 " + hint)
                if s["log"]:
                    st.code(s["log"][-1500:], language="text")
                arts = db.artifacts_of(s)
                for a in arts:
                    st.write(f"📎 {a}")
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("▶ Ejecutar", key=f"run{pid}{s['stage']}",
                                 disabled=bool(_running)):
                        ok, _log = ejecutar_con_progreso(
                            pid, p, s["stage"], gen_fn, sname)
                        if not ok:
                            st.error(_log[-800:])
                        rerun()
                with c2:
                    if st.button("✔ Marcar hecho", key=f"man{pid}{s['stage']}",
                                 disabled=bool(_running)):
                        db.set_stage(conn, pid, s["stage"], "manual",
                                     "Marcado manual desde el panel.")
                        rerun()
                with c3:
                    if st.button("⏭ Omitir", key=f"sk{pid}{s['stage']}",
                                 disabled=bool(_running)):
                        db.set_stage(conn, pid, s["stage"], "omitido", "Omitido.")
                        rerun()

        # ---- puerta: guion ----
        st.subheader("🚪 Puerta 1 · Guion")
        gate = db.get_approval(conn, pid, "guion")
        script_path = pipeline.find_script(p)
        if script_path:
            text = Path(script_path).read_text(encoding="utf-8", errors="replace")
            words = count_words(text)
            st.write(f"**{words} palabras** ≈ {estimate_minutes(words):.1f} min a 155 ppm "
                     f"· estado: **{gate['status']}**")
            with st.expander("Leer guion completo"):
                st.text(text[:20000])
            comment = st.text_area("Comentario (si pides cambios)", key="gc")
            g1, g2, g3 = st.columns(3)
            with g1:
                if st.button("✅ Aprobar guion"):
                    db.set_approval(conn, pid, "guion", "aprobado")
                    db.set_stage(conn, pid, "guion", "ok", "Guion aprobado por humano.")
                    st.success("Guion aprobado. Puedes seguir con «Correr todo».")
                    rerun()
            with g2:
                if st.button("🔁 Pedir cambios"):
                    db.set_approval(conn, pid, "guion", "cambios", comment)
                    st.warning("Marcado para reescritura.")
                    rerun()
            with g3:
                if st.button("🤖 Reescribir con crítica"):
                    try:
                        with st.spinner("Crítico + reescritura (puede tardar)..."):
                            crit, _ = critic_review(gen_fn, text)
                            new, used = draft_script(
                                gen_fn, p["title"],
                                pipeline.prompt_maestro() +
                                "\n\nCRÍTICA A CORREGIR:\n" + crit,
                                target_words=words)
                        outp = pipeline.job_dir_of(p) / "GUION.md"
                        outp.write_text(new, encoding="utf-8")
                        db.set_approval(conn, pid, "guion", "pendiente")
                        db.set_stage(conn, pid, "guion", "en-curso",
                                     f"Reescrito con {used} tras crítica. "
                                     "Pendiente tu aprobación.",
                                     [str(outp)])
                        st.session_state["critic"] = crit
                        st.success("Guion reescrito y guardado en GUION.md. "
                                   "Revísalo y apruébalo.")
                        rerun()
                    except Exception as e:
                        st.error(str(e))
            if "critic" in st.session_state:
                with st.expander("Veredicto del crítico"):
                    st.text(st.session_state["critic"])
        else:
            st.info("Sin guion todavía: pulsa «Correr todo» o ejecuta la etapa 3 (Guion).")

        # ---- puerta: miniatura ----
        st.subheader("🚪 Puerta 2 · Miniatura")
        mgate = db.get_approval(conn, pid, "miniatura")
        thumbs = sorted(pipeline.thumbs_dir().glob(f"thumb_{pid}_*.png"))
        if thumbs:
            cols = st.columns(min(3, len(thumbs)))
            for i, th in enumerate(thumbs[:3]):
                cols[i].image(str(th), caption=th.name)
            choice = st.radio("Elige miniatura", [t.name for t in thumbs[:3]],
                              horizontal=True, key="thumbpick")
            if st.button("✅ Aprobar miniatura"):
                db.set_setting(conn, f"thumb_choice_{pid}", choice)
                db.set_approval(conn, pid, "miniatura", "aprobado", choice)
                db.set_stage(conn, pid, "miniatura", "ok", f"Elegida: {choice}")
                st.success(f"Miniatura elegida: {choice}. "
                           "Ya puedes cerrar el paquete con «Correr todo».")
                rerun()
        else:
            st.info("Sin miniaturas todavía: pulsa «Correr todo» o ejecuta la etapa 9 (Miniaturas).")
        st.caption(f"Estado puerta miniatura: {mgate['status']}")

        # ---- corto-recorte: herramienta ----
        if p["kind"] == "corto-recorte":
            st.subheader("✂️ Recorte del largo")
            srcs = db.list_projects(conn)
            largos = [s for s in srcs if s["kind"] == "largo"]
            if largos:
                src = st.selectbox("Video largo origen",
                                   [f"#{s['id']} {s['title']}" for s in largos])
                src_id = int(src.split()[0][1:])
                sp = db.get_project(conn, src_id)
                vids = sorted(pipeline.job_dir_of(sp).glob("video/*.mp4")) if sp["job_dir"] else []
                vids += [BASE / "jobs/piloto/video/piloto_completo.mp4"]
                vids = [v for v in vids if Path(v).exists()]
                if vids:
                    vpath = st.selectbox("Archivo", [str(v) for v in vids])
                    c1, c2 = st.columns(2)
                    t0 = c1.text_input("Inicio (mm:ss)", "00:30")
                    t1 = c2.text_input("Fin (mm:ss)", "01:15")
                    if st.button("✂️ Generar corto vertical"):
                        dst = BASE / f"jobs/{pid}" / "video" / "corto_vertical.mp4"
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        ok, log = cut_vertical(vpath, dst, t0, t1)
                        db.set_stage(conn, pid, "recorte",
                                     "ok" if ok else "fallo", log,
                                     [str(dst)] if ok else [])
                        if ok:
                            st.success(f"Corto listo: {dst}")
                            st.video(str(dst))
                        else:
                            st.error(log)
                        rerun()


# ============================================================ CONFIG
elif view == "⚙️ Configuración":
    st.title("⚙️ Configuración")
    st.write("**Valores por defecto para proyectos nuevos**")
    import tts_engine
    cur_eng, cur_voice = tts_engine.parse_spec(
        get("default_voice", tts_engine.DEFAULT_SPEC))
    engs = tts_engine.ENGINES
    ceng = st.selectbox(
        "Motor de voz", engs,
        index=engs.index(cur_eng) if cur_eng in engs else 0,
        format_func=lambda e: tts_engine.VOICE_CATALOG[e]["label"])
    vlist = tts_engine.VOICE_CATALOG[ceng]["voices"]
    vids = [v for v, _ in vlist]
    cvoice = st.selectbox(
        "Voz (mujer / hombre · México / España)", vids,
        index=vids.index(cur_voice) if ceng == cur_eng and cur_voice in vids else 0,
        format_func=lambda v: dict(vlist)[v])
    st.caption("Edge = voces neurales de Microsoft, gratis y las más "
               "humanas (internet). Kokoro/Piper = locales, sin internet "
               "(Kokoro necesita espeak-ng instalado).")
    dl = st.text_input("Idioma", get("default_language", "es"))
    if st.button("Guardar defaults"):
        db.set_setting(conn, "default_voice", f"{ceng}:{cvoice}")
        db.set_setting(conn, "default_language", dl)
        st.success("Guardado.")

    st.divider()
    st.write("**Claves de LLM (se guardan en el SQLite local del panel)**")
    st.caption("Todas opcionales: configura al menos un backend en la nube "
               "o usa Ollama local. Sin tarjeta en ningún tier gratis.")
    new_keys = {}
    for b in llm.backend_options():
        meta = llm.BACKENDS[b]
        if not meta["setting"]:
            continue
        new_keys[meta["setting"]] = st.text_input(
            meta["env"], get(meta["setting"]), type="password",
            help=f"{meta['label']} · gratis: {meta['free']}")
    fb = st.text_input(
        "FREELLMAPI_BASE_URL",
        get("freellmapi_base", llm.FREELLMAPI_BASE),
        help="Tu router local es http://localhost:3001/v1 (start-all.bat). "
             "Si usas el hosted: https://api.freellmapi.ai/v1")
    yk = st.text_input("YOUTUBE_API_KEY", get("youtube_key"), type="password",
                       help="Para sugerencias de temas (conector pendiente)")
    if st.button("Guardar claves"):
        for sname, sval in new_keys.items():
            db.set_setting(conn, sname, sval)
        db.set_setting(conn, "freellmapi_base", fb)
        db.set_setting(conn, "youtube_key", yk)
        st.success("Guardado localmente.")

    st.divider()
    st.write("**Modelos Ollama detectados**")
    oms = llm.list_ollama_models()
    if oms:
        for m in oms:
            st.write(f"🖥️ {m}")
    else:
        st.info("Sin servidor Ollama en localhost:11434.")
