#!/usr/bin/env python3
"""Genera miniaturas 1280x720 para los proyectos del panel Zenn Factory.

Uso:
    python generate_thumbnails.py            # todos los proyectos sin miniatura
    python generate_thumbnails.py <id>       # miniaturas del proyecto <id>

Salida: <BASE>/thumbnails/thumb_<id>_<variante>.png  (a, b, c)
Lee el titulo y el guion del proyecto en el SQLite del panel y pinta 3
variantes de miniatura con Pillow. Lo invoca el panel desde la etapa
"miniatura" (pipeline.run_thumbnails).
"""
import os
import sqlite3
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent          # <panel>/thumbnails
PANEL_DIR = HERE.parent                         # carpeta del panel (video-gen)
BASE = PANEL_DIR.parent                         # raiz del proyecto (zenn-factory)
W, H = 1280, 720
FONT_NAMES = ["segoeuib.ttf", "arialbd.ttf", "verdanab.ttf", "calibrib.ttf",
              "segoeui.ttf", "arial.ttf", "verdana.ttf"]
FONTS_DIR = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"

STYLES = [
    {"bg": (15, 18, 32), "fg": (255, 255, 255), "accent": (255, 197, 61),
     "sub": (168, 176, 196), "label": "EL PORQUE"},
    {"bg": (245, 241, 232), "fg": (20, 20, 20), "accent": (232, 68, 46),
     "sub": (92, 88, 80), "label": "EL PORQUE"},
    {"bg_top": (27, 16, 53), "bg_bottom": (74, 26, 97), "fg": (255, 255, 255),
     "accent": (92, 225, 230), "sub": (205, 196, 228), "label": "EL PORQUE"},
]


def find_db():
    for c in (PANEL_DIR / "panel.db", HERE / "panel.db", BASE / "panel.db",
              BASE / "video-gen" / "panel.db"):
        if c.exists():
            return c
    return None


def out_dir(db_path):
    """Carpeta de salida: <raiz>/thumbnails (la que lee el panel)."""
    return db_path.resolve().parent.parent / "thumbnails"


def load_font(size):
    for name in FONT_NAMES:
        p = FONTS_DIR / name
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                continue
    return ImageFont.load_default()


def wrap_lines(draw, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        cand = (cur + " " + word).strip()
        if draw.textlength(cand, font=font) <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, text, max_w, max_h, start=104, min_size=38, step=6):
    size = start
    while True:
        font = load_font(size)
        lines = wrap_lines(draw, text, font, max_w)
        if len(lines) * size * 1.18 <= max_h or size <= min_size:
            max_lines = max(1, int(max_h / (size * 1.18)))
            if len(lines) > max_lines:
                lines = lines[:max_lines]
                while lines and draw.textlength(lines[-1] + "...", font=font) > max_w:
                    lines[-1] = lines[-1][:-1]
                if lines:
                    lines[-1] += "..."
            return font, lines, size
        size -= step


def job_dir_for(row):
    jd = row["job_dir"] or f"jobs/{row['id']}"
    for c in (Path(jd), PANEL_DIR / jd, BASE / jd, HERE / jd):
        if c.exists():
            return c
    return PANEL_DIR / jd


def subtitle_for(job):
    for name in ("GUION.md", "GUION_PILOTO.md", "guion.md"):
        f = job / name
        if f.exists():
            text = f.read_text(encoding="utf-8", errors="replace")
            for para in text.split("\n"):
                para = para.strip()
                if len(para) > 40:
                    return para if len(para) <= 130 else para[:127] + "..."
    return ""


def gradient(top, bottom):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / max(H - 1, 1)
        d.line([(0, y), (W, y)], fill=tuple(
            int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img


def render(title, subtitle, style, path):
    if "bg_top" in style:
        img = gradient(style["bg_top"], style["bg_bottom"])
    else:
        img = Image.new("RGB", (W, H), style["bg"])
    d = ImageDraw.Draw(img, "RGBA")

    acc = style["accent"]
    d.rectangle([0, 0, 18, H], fill=acc)
    d.rectangle([0, 0, W, 8], fill=acc)
    d.ellipse([W - 300, -140, W + 140, 300], fill=acc + (36,))
    d.ellipse([W - 210, H - 190, W + 60, H + 80], fill=acc + (26,))

    label_font = load_font(30)
    d.text((64, 54), style["label"], font=label_font, fill=acc)
    d.text((64 + d.textlength(style["label"], font=label_font) + 18, 60),
           "·  video nuevo", font=load_font(24), fill=style["sub"])

    top, bottom = 140, H - (170 if subtitle else 110)
    font, lines, size = fit_font(d, title, W - 160, bottom - top)
    line_h = size * 1.18
    y = top + ((bottom - top) - len(lines) * line_h) / 2
    for ln in lines:
        d.text((80, y), ln, font=font, fill=style["fg"])
        y += line_h

    if subtitle:
        sfont = load_font(30)
        slines = wrap_lines(d, subtitle, sfont, W - 200)[:2]
        sy = H - 118
        d.rectangle([80, sy - 22, 88, sy + 10], fill=acc)
        for i, sl in enumerate(slines):
            d.text((108, sy + i * 36), sl, font=sfont, fill=style["sub"])

    img.save(path, "PNG")
    return path


def projects(db_path, wanted=None):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, title, job_dir FROM projects ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    if wanted is not None:
        return [r for r in rows if r["id"] == wanted]
    return rows


def main():
    db_path = find_db()
    if not db_path:
        print("No encuentro el panel.db del panel (video-gen/panel.db).", file=sys.stderr)
        return 1

    wanted = int(sys.argv[1]) if len(sys.argv) > 1 else None
    outdir = out_dir(db_path)
    outdir.mkdir(parents=True, exist_ok=True)
    rows = projects(db_path, wanted)
    if wanted is not None and not rows:
        print(f"No existe el proyecto #{wanted}.", file=sys.stderr)
        return 1
    if not rows:
        print("Sin proyectos: nada que generar.")
        return 0

    if wanted is None:
        pendientes = [r for r in rows
                      if not list(outdir.glob(f"thumb_{r['id']}_*.png"))]
        rows = pendientes or rows[:1]

    for r in rows:
        for old in outdir.glob(f"thumb_{r['id']}_*.png"):
            old.unlink()
        title = r["title"].strip() or "Video sin titulo"
        sub = subtitle_for(job_dir_for(r))
        for style, suffix in zip(STYLES, ("a", "b", "c")):
            out = outdir / f"thumb_{r['id']}_{suffix}.png"
            render(title, sub, style, out)
        print(f"Proyecto #{r['id']}: 3 miniaturas -> {outdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
