#!/usr/bin/env python3
"""Panel Zenn Factory — tablero visual del pipeline de videos.

Uso:
    cd ~/workspace/zenn-factory/panel
    pip install -r requirements.txt
    streamlit run app.py
"""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
import db
import llm
import pipeline
from pipeline import (stages_for, count_words, estimate_minutes,
                      propose_topics, draft_script, critic_review,
                      run_tts, run_thumbnails, cut_vertical)

BASE = Path(__file__).resolve().parent.parent

st.set_page_config(page_title="Zenn Factory", layout="wide")

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
    return {"pendiente": "⚪", "en-curso": "🔵", "ok": "🟢",
            "fallo": "🔴", "omitido": "⚫", "manual": "🟡"}.get(status, "❔")


def make_generate_fn(backend, model):
    keys = {b: get(llm.BACKENDS[b]["setting"])
            for b in llm.BACKENDS if llm.BACKENDS[b]["setting"]}
    def fn(prompt, system=""):
        return llm.generate(prompt, backend=backend, model=model,
                             system=system, keys=keys)
    return fn


def all_keys():
    return {b: get(llm.BACKENDS[b]["setting"])
            for b in llm.BACKENDS if llm.BACKENDS[b]["setting"]}


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
    st.sidebar.info(f"Sin {bmeta['env']} — ponla en Configuración.")
else:
    st.sidebar.caption(f"Gratis: {bmeta['free']}")
models = llm.model_options(backend, all_keys())
if backend == "ollama" and not models:
    st.sidebar.warning("Ollama no responde en localhost:11434. Revisa `ollama serve`.")
default_model = get("default_model_id", "")
idx = models.index(default_model) if default_model in models else 0
model_id = st.sidebar.selectbox("Modelo", models or ["(sin modelos)"], index=idx if models else 0)
if st.sidebar.button("Guardar como predeterminado"):
    db.set_setting(conn, "backend", backend)
    db.set_setting(conn, "default_model_id", model_id)
    st.sidebar.success("Guardado.")

st.sidebar.divider()
view = st.sidebar.radio("Vista", ["📥 Bandeja de temas", "🎬 Proyectos",
                                  "⚙️ Configuración"])

# ============================================================ EJECUTORES
def execute_stage(p, stage):
    """Devuelve (ok, log, artifacts)."""
    pid = p["id"]
    job = Path(p["job_dir"]) if p["job_dir"] else BASE / f"jobs/{pid}"
    try:
        if stage == "tts":
            ok, log = run_tts(job, p["voice"], p["language"])
            arts = [str(a) for a in (job / "audio").glob("*.mp3")] if ok else []
            return ok, log, arts
        if stage == "miniatura":
            ok, log = run_thumbnails(pid)
            arts = [str(a) for a in (BASE / "thumbnails").glob(f"thumb_{pid}_*.png")]
            return ok, log, arts
        if stage == "verificacion":
            sp = find_script(p)
            if not sp:
                return False, "Sin guion para verificar.", []
            from pipeline import extract_references
            dois, pmids = extract_references(Path(sp).read_text(encoding="utf-8"))
            log = f"DOIs: {len(dois)}, PMIDs: {len(pmids)}\n" + "\n".join(dois + [f"PMID:{x}" for x in pmids])
            return True, log, []
        return False, f"Etapa '{stage}': sin ejecutor automático todavía. Usa 'Marcar hecho'.", []
    except Exception as e:
        return False, f"Error: {e}", []


def find_script(p):
    job = Path(p["job_dir"]) if p["job_dir"] else BASE / f"jobs/{p['id']}"
    for name in ("GUION_PILOTO.md", "GUION.md", "guion.md"):
        c = job / name
        if c.exists():
            return str(c)
    cands = sorted(job.glob("*.md"))
    return str(cands[0]) if cands else ""


def script_out_path(p):
    job = Path(p["job_dir"]) if p["job_dir"] else BASE / f"jobs/{p['id']}"
    return job / "GUION.md"


# ============================================================ BANDEJA
if view == "📥 Bandeja de temas":
    st.title("📥 Bandeja de temas")
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
                    topics = propose_topics(make_generate_fn(backend, model_id))
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
                    db.set_topic_status(conn, t["id"], "aprobado")
                    st.success(f"Proyecto #{pid} creado ({kind}).")
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
            g = db.get_approval(conn, p["id"], "guion")
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
        st.caption(f"{project_kind_label(p['kind'])} · voz {p['voice']} · "
                   f"{p['language']} · {p['model_backend']}/{p['model_id'] or 'auto'}")

        # ---- config rápida ----
        with st.expander("⚙️ Configuración del proyecto"):
            ck1, ck2, ck3 = st.columns(3)
            nv = ck1.text_input("Voz", p["voice"])
            nl = ck2.text_input("Idioma", p["language"])
            nm = ck3.text_input("Modelo", p["model_id"])
            if st.button("Guardar config"):
                db.update_project(conn, pid, voice=nv, language=nl, model_id=nm)
                st.success("Guardado.")
                rerun()

        # ---- tablero de etapas ----
        st.subheader("Pipeline")
        for s in db.list_stages(conn, pid):
            sname = dict((x[0], x[1]) for x in stages_for(p["kind"])).get(s["stage"], s["stage"])
            auto = dict((x[0], x[2]) for x in stages_for(p["kind"])).get(s["stage"], "?")
            with st.expander(f"{stage_badge(s['status'])} {sname}  ·  `{auto}`"):
                if s["log"]:
                    st.code(s["log"][-1500:], language="text")
                arts = db.artifacts_of(s)
                for a in arts:
                    st.write(f"📎 {a}")
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("▶ Ejecutar", key=f"run{pid}{s['stage']}"):
                        ok, log, arts = execute_stage(p, s["stage"])
                        db.set_stage(conn, pid, s["stage"],
                                     "ok" if ok else "fallo", log, arts)
                        rerun()
                with c2:
                    if st.button("✔ Marcar hecho", key=f"man{pid}{s['stage']}"):
                        db.set_stage(conn, pid, s["stage"], "manual",
                                     "Marcado manual desde el panel.")
                        rerun()
                with c3:
                    if st.button("⏭ Omitir", key=f"sk{pid}{s['stage']}"):
                        db.set_stage(conn, pid, s["stage"], "omitido", "Omitido.")
                        rerun()

        # ---- puerta: guion ----
        st.subheader("🚪 Puerta 1 · Guion")
        gate = db.get_approval(conn, pid, "guion")
        script_path = find_script(p)
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
                    st.success("Guion aprobado.")
                    rerun()
            with g2:
                if st.button("🔁 Pedir cambios"):
                    db.set_approval(conn, pid, "guion", "cambios", comment)
                    st.warning("Marcado para reescritura.")
                    rerun()
            with g3:
                if st.button("🤖 Reescribir con crítica"):
                    try:
                        with st.spinner("Crítico + reescritura..."):
                            crit, _ = critic_review(
                                make_generate_fn(p["model_backend"], p["model_id"] or model_id),
                                text)
                            new, _ = draft_script(
                                make_generate_fn(p["model_backend"], p["model_id"] or model_id),
                                p["title"], "", target_words=words)
                        st.session_state["critic"] = crit
                        st.success("Borrador regenerado (revísalo abajo).")
                    except Exception as e:
                        st.error(str(e))
            if "critic" in st.session_state:
                with st.expander("Veredicto del crítico"):
                    st.text(st.session_state["critic"])
        else:
            st.info("Sin guion todavía. Genéralo en la etapa 'guion'.")
            if st.button("🤖 Generar borrador de guion"):
                pm = (BASE / "PROMPT_MAESTRO.md").read_text(encoding="utf-8", errors="replace")
                try:
                    with st.spinner("Escribiendo..."):
                        target = 150 if p["kind"] != "largo" else 1300
                        txt, used = draft_script(
                            make_generate_fn(p["model_backend"], p["model_id"] or model_id),
                            p["title"], pm, target_words=target)
                    out = script_out_path(p)
                    out.parent.mkdir(parents=True, exist_ok=True)
                    out.write_text(txt, encoding="utf-8")
                    db.set_stage(conn, pid, "guion", "en-curso",
                                 f"Borrador generado con {used}. Pendiente tu aprobación.",
                                 [str(out)])
                    st.success(f"Borrador guardado en {out}. Revísalo arriba.")
                    rerun()
                except Exception as e:
                    st.error(str(e))

        # ---- puerta: miniatura ----
        st.subheader("🚪 Puerta 2 · Miniatura")
        mgate = db.get_approval(conn, pid, "miniatura")
        thumbs = sorted((BASE / "thumbnails").glob(f"thumb_{pid}_*.png"))
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
                st.success(f"Miniatura elegida: {choice}")
                rerun()
        else:
            st.info("Sin miniaturas. Ejecuta la etapa 'miniatura'.")
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
                vids = sorted(Path(sp["job_dir"]).glob("video/*.mp4")) if sp["job_dir"] else []
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
    dv = st.text_input("Voz TTS", get("default_voice", "avocado_v2:MAI_01"))
    dl = st.text_input("Idioma", get("default_language", "es"))
    if st.button("Guardar defaults"):
        db.set_setting(conn, "default_voice", dv)
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
    yk = st.text_input("YOUTUBE_API_KEY", get("youtube_key"), type="password",
                       help="Para sugerencias de temas (conector pendiente)")
    if st.button("Guardar claves"):
        for sname, sval in new_keys.items():
            db.set_setting(conn, sname, sval)
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
