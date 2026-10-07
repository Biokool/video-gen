#!/usr/bin/env python3
"""Genera miniaturas 1280x720 ILUSTRADAS para los proyectos del panel.

Uso:
    python generate_thumbnails.py            # proyectos sin miniatura
    python generate_thumbnails.py <id>       # miniaturas del proyecto <id>

Salida: thumb_<id>_a/b/c.png junto a este script.
Diseño: texto corto y enorme a la izquierda + ilustración grande a la
derecha (monigote + objeto del tema), estilo dibujado a mano (jitter).
Los conceptos (texto/objeto) vienen de concepts_<id>.json si existe
(lo escribe pipeline.run_thumbnails vía LLM); si no, heurística local.
"""
import json
import math
import os
import random
import re
import sqlite3
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1280, 720

WHITE = (255, 255, 255)
BLACK = (17, 17, 17)
YELLOW = (255, 199, 0)
ORANGE = (255, 122, 0)
RED = (230, 57, 70)
TEAL = (42, 157, 143)
BLUE = (64, 140, 255)
GREEN = (74, 190, 110)
PINK = (255, 170, 190)
GOLD = (255, 190, 40)

rng = random.Random(20261001)


# ---------- fuente ----------
def _font_file():
    for c in (HERE / "fonts" / "GochiHand.ttf",
              HERE.parent / "fonts" / "GochiHand.ttf",
              HERE.parent.parent / "fonts" / "GochiHand.ttf"):
        if c.exists():
            return c
    wd = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    for n in ("segoeuib.ttf", "arialbd.ttf", "verdanab.ttf"):
        if (wd / n).exists():
            return wd / n
    return None


FONT_FILE = _font_file()


def font(size):
    if FONT_FILE:
        return ImageFont.truetype(str(FONT_FILE), size)
    try:
        return ImageFont.load_default(size)
    except TypeError:
        return ImageFont.load_default()


# ---------- primitivas dibujadas a mano ----------
def jline(d, pts, width, fill):
    out = []
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        n = max(2, int(math.hypot(x2 - x1, y2 - y1) / 7) + 1)
        for i in range(n):
            t = i / n
            out.append((x1 + (x2 - x1) * t + rng.uniform(-2.4, 2.4),
                        y1 + (y2 - y1) * t + rng.uniform(-2.4, 2.4)))
    out.append(pts[-1])
    d.line(out, fill=fill, width=width, joint="curve")


def hcircle(d, cx, cy, r, width, fill, ry_scale=1.0):
    pts = []
    n = 56
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        rr = r * (1 + rng.uniform(-0.035, 0.035))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * ry_scale))
    d.line(pts, fill=fill, width=width, joint="curve")


def hfill_circle(d, cx, cy, r, fill, outline, ow):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    hcircle(d, cx, cy, r, ow, outline)


def stick(d, x, y, s, pose="point", stroke=BLACK, lw=12):
    """Monigote: x,y = pies; s = altura total."""
    hr = s / 8.0
    hcy = y - s + hr
    shy = y - s * 0.70
    hip = y - s * 0.40
    hcircle(d, x, hcy, hr, lw, stroke)
    if pose == "run":
        shx = x + 0.06 * s
        jline(d, [(shx, shy), (x, hip)], lw, stroke)
        jline(d, [(shx, shy), (x + 0.24 * s, shy + 0.10 * s),
                  (x + 0.32 * s, shy - 0.04 * s)], lw, stroke)
        jline(d, [(shx, shy), (x - 0.18 * s, shy + 0.12 * s),
                  (x - 0.30 * s, shy + 0.04 * s)], lw, stroke)
        jline(d, [(x, hip), (x + 0.22 * s, hip + 0.22 * s),
                  (x + 0.36 * s, y - 0.01 * s)], lw, stroke)
        jline(d, [(x, hip), (x - 0.14 * s, hip + 0.20 * s),
                  (x - 0.36 * s, y - 0.03 * s)], lw, stroke)
    elif pose == "think":
        jline(d, [(x, shy), (x, hip)], lw, stroke)
        jline(d, [(x, shy), (x + 0.16 * s, shy + 0.20 * s),
                  (x + 0.09 * s, hcy + hr * 0.9)], lw, stroke)
        jline(d, [(x, shy), (x - 0.12 * s, shy + 0.24 * s)], lw, stroke)
        jline(d, [(x, hip), (x - 0.10 * s, y)], lw, stroke)
        jline(d, [(x, hip), (x + 0.12 * s, y)], lw, stroke)
    else:  # point
        jline(d, [(x, shy), (x, hip)], lw, stroke)
        jline(d, [(x, shy), (x + 0.30 * s, shy - 0.10 * s),
                  (x + 0.44 * s, shy - 0.12 * s)], lw, stroke)
        jline(d, [(x, shy), (x - 0.12 * s, shy + 0.22 * s)], lw, stroke)
        jline(d, [(x, hip), (x - 0.10 * s, y)], lw, stroke)
        jline(d, [(x, hip), (x + 0.12 * s, y)], lw, stroke)
    return (x, hcy, hr)


# ---------- objetos del tema (props) ----------
def prop_reloj(d, cx, cy, r, lw=11):
    hfill_circle(d, cx - r * 0.78, cy - r * 0.98, r * 0.28, YELLOW, BLACK, lw)
    hfill_circle(d, cx + r * 0.78, cy - r * 0.98, r * 0.28, YELLOW, BLACK, lw)
    jline(d, [(cx - r * 0.58, cy - r * 0.82), (cx - r * 0.34, cy - r * 1.04)], lw, BLACK)
    jline(d, [(cx + r * 0.58, cy - r * 0.82), (cx + r * 0.34, cy - r * 1.04)], lw, BLACK)
    for sx in (-1, 1):
        for i in range(2):
            x0 = cx + sx * r * (1.05 + i * 0.22)
            jline(d, [(x0, cy - r * 1.25), (x0 + sx * 22, cy - r * 1.45)], 8, ORANGE)
    jline(d, [(cx - r * 0.5, cy + r * 0.85), (cx - r * 0.68, cy + r * 1.28)], lw, BLACK)
    jline(d, [(cx + r * 0.5, cy + r * 0.85), (cx + r * 0.68, cy + r * 1.28)], lw, BLACK)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=YELLOW)
    hcircle(d, cx, cy, r, lw + 2, BLACK)
    d.ellipse([cx - r * 0.78, cy - r * 0.78, cx + r * 0.78, cy + r * 0.78], fill=WHITE)
    hcircle(d, cx, cy, r * 0.78, lw - 2, BLACK)
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        d.line([(cx + r * 0.68 * math.cos(a), cy + r * 0.68 * math.sin(a)),
                (cx + r * 0.60 * math.cos(a), cy + r * 0.60 * math.sin(a))],
               fill=BLACK, width=6)
    jline(d, [(cx, cy), (cx - r * 0.35, cy - r * 0.30)], 10, BLACK)
    jline(d, [(cx, cy), (cx + r * 0.15, cy - r * 0.55)], 10, BLACK)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=BLACK)


def prop_calendario(d, cx, cy, w, h, lw=10):
    x, y = cx - w / 2, cy - h / 2
    d.rectangle([x, y, x + w, y + h], fill=WHITE)
    jline(d, [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], lw, BLACK)
    strip = h * 0.18
    d.rectangle([x, y, x + w, y + strip], fill=BLACK)
    for rx in (x + w * 0.28, x + w * 0.72):
        hfill_circle(d, rx, y + strip * 0.45, 12, WHITE, WHITE, 4)
    top, bot = y + strip + 12, y + h - 14
    left, right = x + 14, x + w - 14
    cols, rows = 4, 3
    for i in range(cols + 1):
        xx = left + (right - left) * i / cols
        d.line([(xx, top), (xx, bot)], fill=BLACK, width=4)
    for j in range(rows + 1):
        yy = top + (bot - top) * j / rows
        d.line([(left, yy), (right, yy)], fill=BLACK, width=4)
    ccx = left + (right - left) * 2.5 / cols
    ccy = top + (bot - top) * 1.5 / rows
    cw, chh = (right - left) / cols / 2 - 8, (bot - top) / rows / 2 - 8
    d.rectangle([ccx - cw, ccy - chh, ccx + cw, ccy + chh], fill=RED)


def prop_cerebro(d, cx, cy, r, lw=10):
    d.ellipse([cx - r, cy - r * 0.92, cx + r, cy + r * 0.92], fill=PINK)
    hcircle(d, cx, cy, r, lw, BLACK, ry_scale=0.92)
    # pliegues: arcos internos con jitter
    for (ox, oy, rr) in [(-0.42, -0.30, 0.34), (0.40, -0.34, 0.30),
                         (-0.34, 0.34, 0.30), (0.42, 0.30, 0.34),
                         (0.0, 0.0, 0.26)]:
        hcircle(d, cx + ox * r, cy + oy * r, rr * r, 6, BLACK, ry_scale=0.7)
    jline(d, [(cx, cy - r * 0.9), (cx, cy + r * 0.9)], 6, BLACK)


def prop_tierra(d, cx, cy, r, lw=10):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE)
    for (ox, oy, rx, ry) in [(-0.35, -0.30, 0.34, 0.26), (0.30, -0.05, 0.28, 0.38),
                             (0.05, 0.42, 0.36, 0.24), (-0.48, 0.28, 0.20, 0.18)]:
        d.ellipse([cx + (ox - rx) * r, cy + (oy - ry) * r,
                   cx + (ox + rx) * r, cy + (oy + ry) * r], fill=GREEN)
    hcircle(d, cx, cy, r, lw, BLACK)


def prop_cohete(d, cx, cy, s, lw=10):
    # s = altura total
    w = s * 0.42
    top, bot = cy - s / 2, cy + s / 2
    d.polygon([(cx - w / 2, bot - s * 0.22), (cx - w * 0.78, bot),
               (cx - w / 2, bot)], fill=RED)
    d.polygon([(cx + w / 2, bot - s * 0.22), (cx + w * 0.78, bot),
               (cx + w / 2, bot)], fill=RED)
    d.rectangle([cx - w / 2, top + s * 0.18, cx + w / 2, bot], fill=WHITE)
    jline(d, [(cx - w / 2, top + s * 0.18), (cx - w / 2, bot),
              (cx + w / 2, bot), (cx + w / 2, top + s * 0.18)], lw, BLACK)
    d.polygon([(cx - w / 2, top + s * 0.18), (cx, top), (cx + w / 2, top + s * 0.18)],
              fill=RED)
    hfill_circle(d, cx, cy - s * 0.12, w * 0.26, BLUE, BLACK, 7)
    for i, fx in enumerate((-0.12, 0.0, 0.12)):
        jline(d, [(cx + fx * s, bot), (cx + fx * s * 1.4, bot + s * (0.16 + 0.05 * (i % 2)))],
              9, ORANGE)
    jline(d, [(cx - w / 2, bot), (cx + w / 2, bot)], lw, BLACK)


def prop_bombilla(d, cx, cy, r, lw=10):
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        jline(d, [(cx + r * 1.18 * math.cos(a), cy + r * 1.18 * math.sin(a)),
                  (cx + r * 1.42 * math.cos(a), cy + r * 1.42 * math.sin(a))],
              8, ORANGE)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=YELLOW)
    hcircle(d, cx, cy, r, lw, BLACK)
    d.rectangle([cx - r * 0.34, cy + r * 0.95, cx + r * 0.34, cy + r * 1.45],
                fill=(150, 150, 150))
    jline(d, [(cx - r * 0.34, cy + r * 0.95), (cx - r * 0.34, cy + r * 1.45),
              (cx + r * 0.34, cy + r * 1.45), (cx + r * 0.34, cy + r * 0.95)],
          7, BLACK)


def prop_corazon(d, cx, cy, s, lw=10):
    r = s * 0.30
    d.ellipse([cx - s / 2, cy - s * 0.42, cx - s / 2 + 2 * r, cy - s * 0.42 + 2 * r],
              fill=RED)
    d.ellipse([cx + s / 2 - 2 * r, cy - s * 0.42, cx + s / 2, cy - s * 0.42 + 2 * r],
              fill=RED)
    d.polygon([(cx - s / 2 + 4, cy - s * 0.10), (cx + s / 2 - 4, cy - s * 0.10),
               (cx, cy + s * 0.52)], fill=RED)
    hcircle(d, cx - s / 2 + r, cy - s * 0.42 + r, r, lw, BLACK)
    hcircle(d, cx + s / 2 - r, cy - s * 0.42 + r, r, lw, BLACK)
    jline(d, [(cx - s / 2 + 4, cy - s * 0.10), (cx, cy + s * 0.52),
              (cx + s / 2 - 4, cy - s * 0.10)], lw, BLACK)


def prop_libro(d, cx, cy, w, h, lw=10):
    x, y = cx - w / 2, cy - h / 2
    d.rectangle([x, y, x + w, y + h], fill=RED)
    jline(d, [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], lw, BLACK)
    d.rectangle([x + 16, y + 16, x + w - 16, y + h - 16], fill=WHITE)
    jline(d, [(x + 16, y + 16), (x + w - 16, y + 16), (x + w - 16, y + h - 16),
              (x + 16, y + h - 16), (x + 16, y + 16)], 5, BLACK)
    for i in range(4):
        yy = y + 56 + i * (h - 110) / 3
        jline(d, [(x + 44, yy), (x + w - 44, yy)], 6, BLACK)


def prop_moneda(d, cx, cy, r, lw=10):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    hcircle(d, cx, cy, r, lw, BLACK)
    hcircle(d, cx, cy, r * 0.78, 6, BLACK)
    d.text((cx, cy), "$", font=font(int(r * 1.15)), fill=BLACK, anchor="mm")


def prop_pregunta(d, cx, cy, r, fg=RED):
    hcircle(d, cx, cy, r, 12, fg)
    d.text((cx, cy - r * 0.06), "?", font=font(int(r * 1.5)), fill=fg, anchor="mm")


def prop_agujero(d, cx, cy, r):
    """Hoyo negro: disco de acreción naranja + centro negro brillante."""
    # estrellas
    for (ox, oy) in [(-1.35, -0.85), (1.3, -0.65), (-1.15, 0.75),
                     (1.4, 0.5), (0.15, -1.2), (-0.5, 1.15)]:
        d.ellipse([cx + ox * r - 7, cy + oy * r - 7,
                   cx + ox * r + 7, cy + oy * r + 7], fill=ORANGE)
    box = [cx - r * 1.5, cy - r * 0.44, cx + r * 1.5, cy + r * 0.44]
    d.ellipse(box, outline=ORANGE, width=30)
    d.ellipse(box, outline=YELLOW, width=12)
    # centro negro
    d.ellipse([cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.62],
              fill=BLACK)
    hcircle(d, cx, cy, r * 0.62, 8, YELLOW)
    # arco frontal del disco (pasa POR DELANTE del centro)
    d.arc(box, start=0, end=180, fill=ORANGE, width=30)
    d.arc(box, start=0, end=180, fill=YELLOW, width=12)


def cara_thumb(d, cx, cy, r, tipo="sorpresa", col=BLACK):
    """Cara expresiva sobre la cabeza del monigote (ojos grandes, gesto)."""
    for sx in (-1, 1):
        ex, ey = cx + sx * r * 0.38, cy - r * 0.08
        if tipo == "feliz":
            d.arc([ex - r * 0.20, ey - r * 0.16, ex + r * 0.20, ey + r * 0.20],
                  start=180, end=360, fill=col, width=7)
        elif tipo == "sorpresa":
            d.ellipse([ex - r * 0.21, ey - r * 0.24, ex + r * 0.21,
                       ey + r * 0.24], fill=WHITE, outline=col, width=5)
            d.ellipse([ex - r * 0.08, ey - r * 0.02, ex + r * 0.08,
                       ey + r * 0.14], fill=col)
        else:
            d.ellipse([ex - r * 0.10, ey - r * 0.10, ex + r * 0.10,
                       ey + r * 0.10], fill=col)
        by = cy - r * 0.52
        if tipo == "preocupado":
            d.line([(ex - r * 0.22, by + r * 0.10), (ex + r * 0.22, by - r * 0.12)],
                   fill=col, width=7)
        elif tipo == "sorpresa":
            d.line([(ex - r * 0.22, by - r * 0.14), (ex + r * 0.22, by - r * 0.14)],
                   fill=col, width=7)
        else:
            d.line([(ex - r * 0.22, by), (ex + r * 0.22, by)], fill=col, width=7)
    my = cy + r * 0.42
    if tipo == "feliz":
        d.arc([cx - r * 0.34, my - r * 0.30, cx + r * 0.34, my + r * 0.26],
              start=20, end=160, fill=col, width=8)
    elif tipo == "sorpresa":
        d.ellipse([cx - r * 0.16, my - r * 0.16, cx + r * 0.16, my + r * 0.16],
                  outline=col, width=7)
    elif tipo == "preocupado":
        pts = [(cx - r * 0.3 + i * r * 0.15,
                my + (r * 0.08 if i % 2 else -r * 0.08)) for i in range(5)]
        d.line(pts, fill=col, width=7, joint="curve")
    else:
        d.line([(cx - r * 0.28, my), (cx + r * 0.28, my)], fill=col, width=7)


def prop_perro(d, cx, cy, s):
    """Cara de perro grande (tipo miniatura '¿por qué los perros...?')."""
    r = s
    # orejas caídas
    for sx in (-1, 1):
        d.ellipse([cx + sx * r * 0.95 - r * 0.34, cy - r * 0.95,
                   cx + sx * r * 0.95 + r * 0.34, cy + r * 0.55],
                  fill=(90, 90, 96), outline=BLACK, width=8)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(216, 219, 224),
              outline=BLACK, width=9)
    # hocico
    d.ellipse([cx - r * 0.52, cy + r * 0.18, cx + r * 0.52, cy + r * 0.82],
              fill=WHITE, outline=BLACK, width=6)
    d.ellipse([cx - r * 0.20, cy + r * 0.22, cx + r * 0.20, cy + r * 0.48],
              fill=BLACK)
    d.line([(cx, cy + r * 0.48), (cx, cy + r * 0.62)], fill=BLACK, width=6)
    d.arc([cx - r * 0.3, cy + r * 0.42, cx + r * 0.3, cy + r * 0.78],
          start=20, end=160, fill=BLACK, width=6)
    # ojos grandes
    for sx in (-1, 1):
        ex, ey = cx + sx * r * 0.42, cy - r * 0.28
        d.ellipse([ex - r * 0.17, ey - r * 0.20, ex + r * 0.17, ey + r * 0.20],
                  fill=WHITE, outline=BLACK, width=5)
        d.ellipse([ex - r * 0.08, ey - r * 0.04, ex + r * 0.08, ey + r * 0.12],
                  fill=BLACK)
        d.line([(ex - r * 0.2, ey - r * 0.38), (ex + r * 0.2, ey - r * 0.30)],
               fill=BLACK, width=7)
    # estrella en la frente (dibujada, sin depender de glifos)
    import math as _m
    sp = []
    for i in range(10):
        ang = -_m.pi / 2 + i * _m.pi / 5
        rr = r * 0.30 if i % 2 == 0 else r * 0.13
        sp.append((cx + rr * _m.cos(ang), cy - r * 0.60 + rr * _m.sin(ang)))
    d.polygon(sp, fill=WHITE, outline=BLACK, width=3)


def prop_dino(d, cx, cy, s):
    """Cabeza de T-Rex de perfil con dientes."""
    w, h = s * 2.1, s * 1.25
    x, y = cx - w / 2, cy - h / 2
    d.rounded_rectangle([x, y, x + w, y + h * 0.62], radius=40,
                        fill=(139, 94, 60), outline=BLACK, width=9)
    d.rounded_rectangle([x + w * 0.18, y + h * 0.55, x + w, y + h],
                        radius=30, fill=(139, 94, 60), outline=BLACK, width=9)
    for i in range(5):  # dientes superiores
        tx = x + w * 0.30 + i * w * 0.13
        d.polygon([(tx, y + h * 0.60), (tx + w * 0.09, y + h * 0.60),
                   (tx + w * 0.045, y + h * 0.82)], fill=WHITE,
                  outline=BLACK)
    for i in range(4):  # dientes inferiores
        tx = x + w * 0.36 + i * w * 0.13
        d.polygon([(tx, y + h * 0.98), (tx + w * 0.09, y + h * 0.98),
                   (tx + w * 0.045, y + h * 0.80)], fill=WHITE,
                  outline=BLACK)
    ex, ey = x + w * 0.30, y + h * 0.28
    d.ellipse([ex - 16, ey - 16, ex + 16, ey + 16], fill=BLACK)
    d.ellipse([x + w * 0.78, y + h * 0.30, x + w * 0.86, y + h * 0.42],
              fill=BLACK)  # fosa nasal


def prop_dragon(d, cx, cy, s):
    """Cabeza de dragón verde echando fuego."""
    # llamas primero (salen de la boca, a la izquierda)
    for (fx, fy, fw, fh, col) in [
            (-1.05, 0.25, 0.85, 0.5, ORANGE), (-0.85, 0.18, 0.6, 0.36, YELLOW),
            (-1.25, 0.42, 0.55, 0.3, RED)]:
        d.ellipse([cx + (fx - fw / 2) * s, cy + (fy - fh / 2) * s,
                   cx + (fx + fw / 2) * s, cy + (fy + fh / 2) * s], fill=col)
    w, h = s * 1.7, s * 1.35
    x, y = cx - w / 2 + s * 0.25, cy - h / 2
    d.rounded_rectangle([x, y, x + w, y + h * 0.66], radius=46,
                        fill=(46, 160, 67), outline=BLACK, width=9)
    d.rounded_rectangle([x, y + h * 0.58, x + w * 0.82, y + h], radius=34,
                        fill=(46, 160, 67), outline=BLACK, width=9)
    for sx in (0.18, 0.52):  # cuernos
        hx = x + w * sx
        d.polygon([(hx, y + 6), (hx + w * 0.10, y - s * 0.34),
                   (hx + w * 0.20, y + 4)], fill=(240, 230, 200),
                  outline=BLACK)
    for i in range(4):
        tx = x + w * 0.08 + i * w * 0.16
        d.polygon([(tx, y + h * 0.64), (tx + w * 0.10, y + h * 0.64),
                   (tx + w * 0.05, y + h * 0.84)], fill=WHITE, outline=BLACK)
    ex, ey = x + w * 0.62, y + h * 0.30
    d.ellipse([ex - 17, ey - 20, ex + 17, ey + 20], fill=WHITE,
              outline=BLACK, width=5)
    d.ellipse([ex - 7, ey - 9, ex + 7, ey + 9], fill=BLACK)
    d.line([(ex - 26, ey - 42), (ex + 26, ey - 34)], fill=BLACK, width=8)


def prop_curva(d, cx, cy, s):
    """Curva campana con punto rojo y flecha (gráficos virales)."""
    import math as _m
    col = WHITE if CURRENT_BG == BLACK else BLACK
    pts = []
    for i in range(81):
        t = -1.6 + 3.2 * i / 80
        pts.append((cx + t * s * 0.62,
                    cy + s * 0.55 - s * 0.95 * _m.exp(-(t ** 2) / 0.9)))
    d.line(pts, fill=col, width=14, joint="curve")
    d.line([(cx - s * 1.05, cy + s * 0.58), (cx + s * 1.05, cy + s * 0.58)],
           fill=col, width=8)
    d.ellipse([cx - 20, cy - s * 0.52, cx + 20, cy - s * 0.52 + 40],
              fill=RED, outline=BLACK, width=4)
    d.line([(cx + s * 0.42, cy - s * 0.95), (cx + s * 0.08, cy - s * 0.60)],
           fill=RED, width=12)
    d.polygon([(cx + s * 0.02, cy - s * 0.52), (cx + s * 0.20, cy - s * 0.62),
               (cx + s * 0.05, cy - s * 0.72)], fill=RED)


def prop_lapida(d, cx, cy, s):
    w, h = s * 1.5, s * 1.8
    x, y = cx - w / 2, cy - h / 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=int(w * 0.45),
                        fill=(178, 184, 194), outline=BLACK, width=9)
    d.text((cx, cy - s * 0.18), "RIP", font=font(int(s * 0.52)), fill=BLACK,
           anchor="mm")
    d.line([(x - 14, y + h), (x + w + 14, y + h)], fill=BLACK, width=9)
    for gx in (-0.55, -0.2, 0.25, 0.6):
        d.line([(cx + gx * s, y + h), (cx + gx * s + 8, y + h - s * 0.22)],
               fill=TEAL, width=7)


CURRENT_BG = BLACK  # render() lo fija antes de dibujar el prop


def prop_luna(d, cx, cy, s):
    """Luna creciente: círculo amarillo recortado con el color de fondo."""
    d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=YELLOW,
              outline=BLACK, width=7)
    d.ellipse([cx - s * 0.42, cy - s * 1.02, cx + s * 0.98, cy + s * 0.62],
              fill=CURRENT_BG)
    d.arc([cx - s, cy - s, cx + s, cy + s], start=100, end=265, fill=BLACK,
          width=7)
    for (sx, sy, sr) in [(-0.85, -0.75, 0.10), (0.75, 0.85, 0.08),
                         (-0.95, 0.45, 0.07)]:
        ex, ey = cx + sx * s * 1.25, cy + sy * s
        d.line([(ex - sr * s, ey), (ex + sr * s, ey)], fill=WHITE, width=5)
        d.line([(ex, ey - sr * s), (ex, ey + sr * s)], fill=WHITE, width=5)


PROPS = {
    "reloj": lambda d, cx, cy: prop_reloj(d, cx, cy, 150),
    "calendario": lambda d, cx, cy: prop_calendario(d, cx, cy, 330, 300),
    "cerebro": lambda d, cx, cy: prop_cerebro(d, cx, cy, 165),
    "tierra": lambda d, cx, cy: prop_tierra(d, cx, cy, 165),
    "cohete": lambda d, cx, cy: prop_cohete(d, cx, cy, 380),
    "bombilla": lambda d, cx, cy: prop_bombilla(d, cx, cy, 130),
    "corazon": lambda d, cx, cy: prop_corazon(d, cx, cy, 330),
    "libro": lambda d, cx, cy: prop_libro(d, cx, cy, 300, 360),
    "moneda": lambda d, cx, cy: prop_moneda(d, cx, cy, 160),
    "pregunta": lambda d, cx, cy: prop_pregunta(d, cx, cy, 170),
    "agujero": lambda d, cx, cy: prop_agujero(d, cx, cy, 165),
    "perro": lambda d, cx, cy: prop_perro(d, cx, cy, 175),
    "dino": lambda d, cx, cy: prop_dino(d, cx, cy, 165),
    "dragon": lambda d, cx, cy: prop_dragon(d, cx, cy, 165),
    "curva": lambda d, cx, cy: prop_curva(d, cx, cy, 165),
    "lapida": lambda d, cx, cy: prop_lapida(d, cx, cy, 165),
    "luna": lambda d, cx, cy: prop_luna(d, cx, cy, 165),
}

STYLES = [
    {"bg": YELLOW, "fg": BLACK, "stroke": BLACK, "pose": "run",
     "expr": "feliz", "playera": "naranja"},
    {"bg": BLACK, "fg": WHITE, "stroke": WHITE, "pose": "point",
     "expr": "sorpresa", "playera": "azul"},
    {"bg": WHITE, "fg": BLACK, "stroke": BLACK, "pose": "think",
     "expr": "preocupado", "playera": "roja"},
]


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        cand = (cur + " " + word).strip()
        if draw.textlength(cand, font=fnt) <= max_w or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, max_w, max_h, start=170):
    size = start
    while size >= 40:
        f = font(size)
        lines = wrap(draw, text, f, max_w)
        if len(lines) * size * 1.12 <= max_h and len(lines) <= 3:
            return f, lines, size
        size -= 8
    f = font(40)
    return f, wrap(draw, text, f, max_w)[:3], 40


def render(concept, style, path, seed):
    global CURRENT_BG
    CURRENT_BG = style["bg"]
    rng.seed(seed)
    img = Image.new("RGB", (W, H), style["bg"])
    d = ImageDraw.Draw(img)
    fg, stroke = style["fg"], style["stroke"]
    # suelo
    jline(d, [(690, 648), (1245, 648)], 8, stroke)
    # protagonista oficial señalando al objeto, con cara expresiva
    # (expresión y playera vienen del concepto; el estilo da el default)
    prota_thumb(d, 790, 648, 330,
                playera=concept.get("playera",
                                    style.get("playera", "naranja")),
                expr=concept.get("expr", style.get("expr", "sorpresa")),
                pose=style["pose"], stroke=stroke)
    # objeto del tema, grande
    PROPS.get(concept.get("prop", "pregunta"),
              PROPS["pregunta"])(d, 1085, 325)
    # texto enorme a la izquierda
    f, lines, size = fit_text(d, concept["text"].upper(), 560, 430)
    y = 150 + (430 - len(lines) * size * 1.12) / 2
    for ln in lines:
        d.text((64, y), ln, font=f, fill=fg,
               stroke_width=2, stroke_fill=fg)
        y += size * 1.12
    # marca del canal
    d.text((64, H - 62), "EL PORQUÉ", font=font(40), fill=fg,
           stroke_width=1, stroke_fill=fg)
    img.save(path, "PNG")
    return path


# ---------- conceptos (fallback sin LLM) ----------
_KEYWORD_PROPS = [
    (("hoyo negro", "agujero negro", "agujero"), "agujero"),
    (("perro", "perros", "cachorro", "mascota"), "perro"),
    (("dinosaurio", "t-rex", "trex", "fósil", "fosil"), "dino"),
    (("dragón", "dragon", "dragones"), "dragon"),
    (("tumba", "tumbas", "cementerio", "muerto", "muerte"), "lapida"),
    (("felicidad", "felices", "feliz"), "curva"),
    (("vikingo", "noche", "oscuro", "oscuridad", "miedo a la"), "luna"),
    (("tiempo", "reloj", "edad", "envejec"), "reloj"),
    (("calendario", "año", "mes"), "calendario"),
    (("cerebro", "mente", "memoria", "sueño"), "cerebro"),
    (("tierra", "planeta", "clima", "océano"), "tierra"),
    (("espacio", "luna", "marte", "universo"), "cohete"),
    (("idea", "luz", "invento"), "bombilla"),
    (("salud", "corazón", "cuerpo"), "corazon"),
    (("historia", "libro", "antigu"), "libro"),
    (("dinero", "precio", "cuesta"), "moneda"),
]


_STOPWORDS = {"qué", "que", "cómo", "como", "por", "si", "pasaría", "pasaria",
              "en", "un", "una", "el", "la", "los", "las", "de", "del", "al",
              "a", "y", "o", "es", "son", "cuándo", "cuando", "dónde", "donde"}


def fallback_concepts(title):
    t = title.lower()
    prop = "pregunta"
    for keys, name in _KEYWORD_PROPS:
        if any(k in t for k in keys):
            prop = name
            break
    clean = re.sub(r"[¿?¡!]", " ", title).lower().strip()
    clean = re.sub(r"^(por qué|porque)\s+", "", clean)
    words = [w for w in clean.split() if w not in _STOPWORDS] or clean.split()
    # palabras gancho: primero cifras/mayúsculas del título, luego las más
    # largas (sustantivos); máx 4 para impacto en miniatura
    scored = []
    for w in words:
        s = len(w) * 2 + (10 if any(c.isdigit() for c in w) else 0)
        if w.upper() in title.upper().split():
            s += 3
        scored.append((s, w))
    scored.sort(reverse=True)
    hook = [w for _, w in scored[:4]]
    text = " ".join(hook).upper() or "EL PORQUÉ"
    expr = "preocupado" if any(k in t for k in
                               ("miedo", "peligro", "veneno", "guerra",
                                "error", "desastre")) else "sorpresa"
    return [{"text": text, "prop": prop, "expr": expr, "playera": "naranja"},
            {"text": text, "prop": "pregunta", "expr": "sorpresa",
             "playera": "azul"},
            {"text": text, "prop": prop, "expr": expr, "playera": "verde"}]


def find_db():
    for c in (HERE.parent / "panel.db", HERE.parent / "panel" / "panel.db",
              HERE / "panel.db"):
        if c.exists():
            return c
    return None


def project_title(db_path, pid):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT title FROM projects WHERE id=?", (pid,)).fetchone()
    conn.close()
    return row["title"] if row else ""


def all_project_ids(db_path):
    conn = sqlite3.connect(str(db_path))
    rows = conn.execute("SELECT id FROM projects ORDER BY id").fetchall()
    conn.close()
    return [r[0] for r in rows]


def main():
    wanted = int(sys.argv[1]) if len(sys.argv) > 1 else None
    db_path = find_db()
    if wanted is None:
        if not db_path:
            print("Sin panel.db y sin id: nada que generar.", file=sys.stderr)
            return 1
        ids = [i for i in all_project_ids(db_path)
               if not list(HERE.glob(f"thumb_{i}_*.png"))]
        ids = ids or all_project_ids(db_path)[:1]
    else:
        ids = [wanted]
    for pid in ids:
        cfile = HERE / f"concepts_{pid}.json"
        concepts = None
        if cfile.exists():
            try:
                concepts = json.loads(cfile.read_text(encoding="utf-8"))
            except Exception:
                concepts = None
        if not concepts:
            title = project_title(db_path, pid) if db_path else ""
            concepts = fallback_concepts(title or "El Porqué")
        for old in HERE.glob(f"thumb_{pid}_*.png"):
            old.unlink()
        for style, suffix, concept in zip(STYLES, ("a", "b", "c"), concepts):
            out = HERE / f"thumb_{pid}_{suffix}.png"
            render(concept, style, out, seed=20261001 + pid * 10 + ord(suffix))
            kb = out.stat().st_size / 1024
            print(f"{out.name}: 1280x720, {kb:.0f} KB "
                  f"[texto='{concept['text']}' objeto={concept['prop']}]")
    return 0


# ---------- protagonista "El Porqué" para miniaturas ----------
PLAYERA_T = {
    "naranja": (245, 130, 11), "azul": (46, 155, 230),
    "verde": (63, 163, 77), "roja": (230, 57, 70),
    "amarilla": (255, 195, 0), "rosa": (242, 92, 155),
    "teal": (42, 157, 143), "morada": (123, 47, 190),
    "negra": (34, 34, 34), "blanca": (245, 245, 245),
}


def prota_thumb(d, x, y, s, playera="naranja", expr="sorpresa",
                pose="point", stroke=BLACK, lw=12):
    """Protagonista oficial: x,y = pies; s = altura total."""
    col = PLAYERA_T.get(playera, PLAYERA_T["naranja"])
    fs = (17, 17, 17)  # la cara siempre en oscuro (la cabeza es blanca)
    hr = s * 0.20  # proporciones alargadas (rig v4.1)
    hcx, hcy = x, y - s + hr
    # cabeza
    d.ellipse([hcx - hr, hcy - hr, hcx + hr, hcy + hr],
              fill=WHITE, outline=fs, width=lw)
    # ojos grandes
    for sx in (-1, 1):
        ex, ey = hcx + sx * hr * 0.36, hcy + hr * 0.08
        ew, eh = hr * 0.64, hr * 0.88
        d.ellipse([ex - ew / 2, ey - eh / 2, ex + ew / 2, ey + eh / 2],
                  fill=WHITE, outline=fs, width=max(4, lw // 2))
        pr = hr * 0.20
        d.ellipse([ex - pr, ey - pr * 0.6, ex + pr, ey + pr * 1.4],
                  fill=fs)
        br = pr * 0.36
        d.ellipse([ex - br * 1.6, ey - br * 0.6, ex - br * 0.2, ey + br * 0.8],
                  fill=WHITE)
    # boca
    my = hcy + hr * 0.52
    if expr == "feliz":
        d.arc([hcx - hr * 0.34, my - hr * 0.34, hcx + hr * 0.34, my + hr * 0.34],
              start=20, end=160, fill=fs, width=max(5, lw // 2))
    elif expr == "preocupado":
        d.arc([hcx - hr * 0.30, my - hr * 0.10, hcx + hr * 0.30, my + hr * 0.42],
              start=200, end=340, fill=fs, width=max(5, lw // 2))
    else:  # sorpresa
        d.ellipse([hcx - hr * 0.16, my - hr * 0.18, hcx + hr * 0.16,
                   my + hr * 0.18], fill=fs)
    # playera: torso (sin mangas)
    tw, th = s * 0.24, s * 0.20
    ttop = hcy + hr + s * 0.03
    d.rounded_rectangle([x - tw / 2, ttop, x + tw / 2, ttop + th],
                        radius=int(s * 0.06), fill=col, outline=stroke,
                        width=max(6, lw - 2))
    # extremidades
    shy, hip = ttop + s * 0.05, ttop + th
    if pose == "run":
        jline(d, [(x + 0.06 * s, shy), (x, hip)], lw, stroke)
        jline(d, [(x + 0.06 * s, shy), (x + 0.30 * s, shy - 0.06 * s)], lw, stroke)
        jline(d, [(x + 0.06 * s, shy), (x - 0.20 * s, shy + 0.10 * s)], lw, stroke)
        jline(d, [(x, hip), (x + 0.30 * s, y - 0.02 * s)], lw, stroke)
        jline(d, [(x, hip), (x - 0.26 * s, y - 0.02 * s)], lw, stroke)
    elif pose == "think":
        jline(d, [(x, shy), (x, hip)], lw, stroke)
        jline(d, [(x, shy), (x + 0.14 * s, shy + 0.18 * s),
                  (x + 0.08 * s, hcy + hr * 0.8)], lw, stroke)
        jline(d, [(x, shy), (x - 0.12 * s, shy + 0.20 * s)], lw, stroke)
        jline(d, [(x, hip), (x - 0.10 * s, y)], lw, stroke)
        jline(d, [(x, hip), (x + 0.12 * s, y)], lw, stroke)
    else:  # point
        jline(d, [(x, shy), (x, hip)], lw, stroke)
        jline(d, [(x, shy), (x + 0.34 * s, shy - 0.06 * s)], lw, stroke)
        jline(d, [(x, shy), (x - 0.12 * s, shy + 0.20 * s)], lw, stroke)
        jline(d, [(x, hip), (x - 0.10 * s, y)], lw, stroke)
        jline(d, [(x, hip), (x + 0.12 * s, y)], lw, stroke)
    return (hcx, hcy, hr)


if __name__ == "__main__":
    sys.exit(main())
