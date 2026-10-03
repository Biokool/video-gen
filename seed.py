#!/usr/bin/env python3
"""Siembra el panel con el piloto ya producido (una sola vez)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import db
from pipeline import stages_for

conn = db.connect()
db.init_db()

# Evita duplicar
if conn.execute("SELECT COUNT(*) c FROM projects").fetchone()["c"]:
    print("Ya hay proyectos. Nada que sembrar.")
    sys.exit(0)

tid = db.add_topic(
    conn,
    "¿Por qué el tiempo pasa más rápido cuando envejeces?",
    "La percepción del tiempo se acelera con la edad",
    source="manual",
    signals="Pregunta universal, alto potencial de retención",
    notes="Video piloto del canal El Porqué",
)
db.set_topic_status(conn, tid, "aprobado")

pid = db.add_project(
    conn,
    "¿Por qué el tiempo pasa más rápido cuando envejeces?",
    topic_id=tid, kind="largo",
    voice="edge:es-MX-DaliaNeural", language="es",
    model_backend="openrouter", model_id="",
    job_dir="jobs/piloto",
)
db.ensure_stages(conn, pid, [s for s, _, _ in stages_for("largo")])
db.ensure_approvals(conn, pid)
db.set_approval(conn, pid, "tema", "aprobado", "Piloto")

# El piloto está producido hasta miniatura; paquete queda pendiente
hechas = ["tema", "investigacion", "guion", "verificacion", "storyboard",
          "tts", "animacion", "ensamblado", "miniatura"]
for s in hechas:
    db.set_stage(conn, pid, s, "ok", "Producido en la sesión del 2026-10-01.")
db.set_approval(conn, pid, "guion", "aprobado", "Guion piloto v1")
db.set_setting(conn, "default_voice", "edge:es-MX-DaliaNeural")
db.set_setting(conn, "default_language", "es")
db.set_setting(conn, "backend", "openrouter")
print(f"Seed OK: proyecto #{pid} con {len(hechas)}/10 etapas en ok.")
