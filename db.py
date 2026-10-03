#!/usr/bin/env python3
"""Capa de persistencia del panel Zenn Factory (SQLite local).

Tablas:
  topics    - bandeja de temas (manuales, LLM o YouTube)
  projects  - cada video (largo | corto-recorte | corto-standalone)
  stages    - estado de cada etapa del pipeline por proyecto
  approvals - las 3 puertas: tema, guion, miniatura
  settings  - ajustes globales (defaults, API keys)
"""
import json
import sqlite3
import time
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "panel.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    angle TEXT DEFAULT '',
    source TEXT DEFAULT 'manual',          -- manual | llm | youtube
    signals TEXT DEFAULT '',               -- por qué puede funcionar
    status TEXT DEFAULT 'propuesto',       -- propuesto | aprobado | rechazado | archivado
    notes TEXT DEFAULT '',
    created_at REAL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER REFERENCES topics(id),
    title TEXT NOT NULL,
    kind TEXT DEFAULT 'largo',             -- largo | corto-recorte | corto-standalone
    voice TEXT DEFAULT 'edge:es-MX-DaliaNeural',
    language TEXT DEFAULT 'es',
    model_backend TEXT DEFAULT 'openrouter', -- openrouter | ollama
    model_id TEXT DEFAULT '',
    status TEXT DEFAULT 'idea',
    job_dir TEXT DEFAULT '',
    created_at REAL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS stages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER REFERENCES projects(id),
    stage TEXT NOT NULL,
    status TEXT DEFAULT 'pendiente',       -- pendiente | en-curso | ok | fallo | omitido | manual
    started_at REAL DEFAULT 0,
    finished_at REAL DEFAULT 0,
    log TEXT DEFAULT '',
    artifacts TEXT DEFAULT '[]',           -- JSON list de rutas
    UNIQUE(project_id, stage)
);
CREATE TABLE IF NOT EXISTS approvals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER REFERENCES projects(id),
    gate TEXT NOT NULL,                    -- tema | guion | miniatura
    status TEXT DEFAULT 'pendiente',       -- pendiente | aprobado | cambios
    comment TEXT DEFAULT '',
    decided_at REAL DEFAULT 0,
    UNIQUE(project_id, gate)
);
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT DEFAULT ''
);
"""


def connect(path=DB_PATH):
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path=DB_PATH):
    conn = connect(path)
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


# ---- settings ----
def get_setting(conn, key, default=""):
    row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    return row["value"] if row else default


def set_setting(conn, key, value):
    conn.execute(
        "INSERT INTO settings(key, value) VALUES(?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )
    conn.commit()


# ---- topics ----
def add_topic(conn, question, angle="", source="manual", signals="", notes=""):
    cur = conn.execute(
        "INSERT INTO topics(question, angle, source, signals, notes, created_at)"
        " VALUES(?,?,?,?,?,?)",
        (question, angle, source, signals, notes, time.time()),
    )
    conn.commit()
    return cur.lastrowid


def list_topics(conn, status=None):
    q = "SELECT * FROM topics ORDER BY created_at DESC"
    args = ()
    if status:
        q = "SELECT * FROM topics WHERE status=? ORDER BY created_at DESC"
        args = (status,)
    return conn.execute(q, args).fetchall()


def set_topic_status(conn, topic_id, status):
    conn.execute("UPDATE topics SET status=? WHERE id=?", (status, topic_id))
    conn.commit()


# ---- projects ----
def add_project(conn, title, topic_id=None, kind="largo", voice=None, language="es",
                model_backend="openrouter", model_id="", job_dir=""):
    if voice is None:
        voice = get_setting(conn, "default_voice", "edge:es-MX-DaliaNeural")
    cur = conn.execute(
        "INSERT INTO projects(topic_id, title, kind, voice, language,"
        " model_backend, model_id, job_dir, created_at)"
        " VALUES(?,?,?,?,?,?,?,?,?)",
        (topic_id, title, kind, voice, language, model_backend, model_id,
         job_dir, time.time()),
    )
    conn.commit()
    return cur.lastrowid


def list_projects(conn):
    return conn.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()


def get_project(conn, project_id):
    return conn.execute("SELECT * FROM projects WHERE id=?", (project_id,)).fetchone()


def update_project(conn, project_id, **fields):
    sets = ", ".join(f"{k}=?" for k in fields)
    conn.execute(f"UPDATE projects SET {sets} WHERE id=?",
                 (*fields.values(), project_id))
    conn.commit()


# ---- stages ----
def ensure_stages(conn, project_id, stage_names):
    for s in stage_names:
        conn.execute(
            "INSERT OR IGNORE INTO stages(project_id, stage) VALUES(?, ?)",
            (project_id, s),
        )
    conn.commit()


def list_stages(conn, project_id):
    return conn.execute(
        "SELECT * FROM stages WHERE project_id=? ORDER BY id", (project_id,)
    ).fetchall()


def set_stage(conn, project_id, stage, status, log="", artifacts=None):
    now = time.time()
    if status == "en-curso":
        conn.execute(
            "UPDATE stages SET status=?, started_at=?, log=? "
            "WHERE project_id=? AND stage=?",
            (status, now, log, project_id, stage),
        )
    else:
        arts = json.dumps(artifacts or [])
        conn.execute(
            "UPDATE stages SET status=?, finished_at=?, log=?, artifacts=? "
            "WHERE project_id=? AND stage=?",
            (status, now, log, arts, project_id, stage),
        )
    conn.commit()


def stage_progress(conn, project_id):
    rows = list_stages(conn, project_id)
    total = len(rows)
    done = sum(1 for r in rows if r["status"] in ("ok", "omitido", "manual"))
    return done, total


# ---- approvals ----
def ensure_approvals(conn, project_id):
    for g in ("tema", "guion", "miniatura"):
        conn.execute(
            "INSERT OR IGNORE INTO approvals(project_id, gate) VALUES(?, ?)",
            (project_id, g),
        )
    conn.commit()


def get_approval(conn, project_id, gate):
    return conn.execute(
        "SELECT * FROM approvals WHERE project_id=? AND gate=?",
        (project_id, gate),
    ).fetchone()


def set_approval(conn, project_id, gate, status, comment=""):
    conn.execute(
        "UPDATE approvals SET status=?, comment=?, decided_at=? "
        "WHERE project_id=? AND gate=?",
        (status, comment, time.time(), project_id, gate),
    )
    conn.commit()


def artifacts_of(stage_row):
    try:
        return json.loads(stage_row["artifacts"] or "[]")
    except Exception:
        return []
