"""
Zenn Factory — Rig de monigotes y primitivas de animación (Manim).

Implementa el vocabulario visual restringido de BIBLIA.md §7.
Todas las coordenadas están en unidades Manim (frame 14.22 x 8.0).

Uso:
    from zenn_rig import StickFigure, title_card, callout, WalkTo, ...

    class MiEscena(Scene):
        def construct(self):
            fig = stick_idle(LEFT * 4)
            self.play(FadeIn(fig))
            self.play(stick_walk(fig, RIGHT * 4, run_time=2.5))
"""

import numpy as np
from manim import (
    VGroup, Circle, Line, Rectangle, Ellipse, Text, Arrow,
    FadeIn, FadeOut, GrowFromCenter, Create,
    Animation, ORIGIN, LEFT, RIGHT, UP, DOWN, PI,
    ParametricFunction, DashedVMobject,
    config,
)

# ---------------------------------------------------------------- paleta (BIBLIA.md §1)
WHITE  = "#FFFFFF"
INK    = "#111111"
YELLOW = "#FFC700"
ORANGE = "#FF7A00"
RED    = "#E63946"
TEAL   = "#2A9D8F"

config.pixel_width = 1280
config.pixel_height = 720
config.background_color = WHITE  # BIBLIA.md §1: fondo principal blanco

FONT = "DejaVu Sans"   # fallback; producción: Gochi Hand (ver BIBLIA.md §1)


# ---------------------------------------------------------------- monigote
class StickFigure(VGroup):
    """Monigote paramétrico. La posición se controla vía `_base` (pies).

    Toda la geometría se recalcula con refresh(), así nunca hay
    desfases de coordenadas al animar a mano.
    """

    def __init__(self, height=2.2, color=INK, stroke_width=10, base=ORIGIN):
        super().__init__()
        self.fig_height = height
        self.color = color
        self.sw = stroke_width
        self._base = np.array(base, dtype=float)

        self.head = Circle(radius=height * 0.13, color=color,
                           stroke_width=stroke_width)
        self.torso = Line(ORIGIN, ORIGIN, color=color, stroke_width=stroke_width)
        self.leg_l = Line(ORIGIN, ORIGIN, color=color, stroke_width=stroke_width)
        self.leg_r = Line(ORIGIN, ORIGIN, color=color, stroke_width=stroke_width)
        self.arm_l = Line(ORIGIN, ORIGIN, color=color, stroke_width=stroke_width)
        self.arm_r = Line(ORIGIN, ORIGIN, color=color, stroke_width=stroke_width)
        self.add(self.head, self.torso,
                 self.leg_l, self.leg_r, self.arm_l, self.arm_r)
        self.refresh(0.0, 0.0)

    # -- geometría -------------------------------------------------
    def refresh(self, leg_swing=0.0, arm_swing=0.0):
        b, h = self._base, self.fig_height
        head_r = h * 0.13
        neck = b + np.array([0.0, h - 2 * head_r, 0.0])
        hip = b + np.array([0.0, h * 0.30, 0.0])
        shoulder = b + np.array([0.0, h - 2 * head_r - h * 0.06, 0.0])

        self.head.move_to(b + np.array([0.0, h - head_r, 0.0]))
        self.torso.put_start_and_end_on(neck, hip)

        for leg, s in ((self.leg_l, leg_swing), (self.leg_r, -leg_swing)):
            self._limb(leg, hip, h * 0.30, -PI / 2 + s * 0.55)
        for arm, s in ((self.arm_l, -arm_swing), (self.arm_r, arm_swing)):
            self._limb(arm, shoulder, h * 0.30, -PI / 2 + s * 0.50 - 0.12)

    @staticmethod
    def _limb(line, start, length, ang):
        end = start + length * np.array([np.cos(ang), np.sin(ang), 0.0])
        line.put_start_and_end_on(start, end)

    # -- API pública -----------------------------------------------
    def set_base(self, p):
        """Teletransporta al monigote (fuera de animación)."""
        self._base = np.array(p, dtype=float)
        self.refresh(0.0, 0.0)
        return self

    def point(self, target):
        """Brazo derecho señalando a `target` (coordenada mundo)."""
        b, h = self._base, self.fig_height
        head_r = h * 0.13
        shoulder = b + np.array([0.0, h - 2 * head_r - h * 0.06, 0.0])
        target = np.array(target, dtype=float)
        vec = target - shoulder
        dist = max(np.linalg.norm(vec[:2]), 1e-6)
        end = shoulder + vec / dist * (h * 0.34)
        self.arm_r.put_start_and_end_on(shoulder, end)
        return self

    def think_bubble(self, text, width=3.2):
        """Nube de pensamiento sobre la cabeza. Devuelve VGroup."""
        b, h = self._base, self.fig_height
        top = b + np.array([0.0, h + 0.55, 0.0])
        bubble = Ellipse(width=width, height=width * 0.55,
                         color=self.color, stroke_width=6)
        bubble.move_to(top + RIGHT * 0.4)
        c1 = Circle(radius=0.09, color=self.color, stroke_width=5)
        c1.move_to(b + np.array([0.15, h + 0.12, 0.0]))
        c2 = Circle(radius=0.14, color=self.color, stroke_width=5)
        c2.move_to(b + np.array([0.35, h + 0.32, 0.0]))
        label = Text(text, font=FONT, font_size=28, color=self.color)
        # encoge el texto si no cabe
        if label.width > width * 0.85:
            label.scale((width * 0.85) / label.width)
        label.move_to(bubble.get_center())
        return VGroup(c1, c2, bubble, label)


# ---------------------------------------------------------------- animación de marcha
class WalkTo(Animation):
    """Desplaza al monigote de su base actual a `target` oscilando
    piernas/brazos. Al terminar deja pose neutra."""

    def __init__(self, figure, target, steps=6, run_time=2.0, **kwargs):
        super().__init__(figure, run_time=run_time, **kwargs)
        self._target = np.array(target, dtype=float)
        self._steps = steps

    def interpolate_mobject(self, alpha):
        fig = self.mobject
        if not hasattr(self, "_start"):
            self._start = fig._base.copy()
        fig._base = self._start * (1 - alpha) + self._target * alpha
        swing = float(np.sin(alpha * self._steps * 2 * np.pi))
        fig.refresh(leg_swing=swing, arm_swing=swing)

    def finish(self):
        self.mobject._base = self._target.copy()
        self.mobject.refresh(0.0, 0.0)
        super().finish()


class RunTo(WalkTo):
    """Como WalkTo pero con zancada más rápida y amplia."""

    def __init__(self, figure, target, steps=10, run_time=1.5, **kwargs):
        super().__init__(figure, target, steps=steps,
                         run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha):
        fig = self.mobject
        if not hasattr(self, "_start"):
            self._start = fig._base.copy()
        fig._base = self._start * (1 - alpha) + self._target * alpha
        swing = float(np.sin(alpha * self._steps * 2 * np.pi)) * 1.25
        swing = max(-1.0, min(1.0, swing))
        fig.refresh(leg_swing=swing, arm_swing=swing)


# ---------------------------------------------------------------- primitivas (BIBLIA.md §7)
def title_card(text, color=YELLOW):
    """Tarjeta de capítulo a pantalla completa."""
    bg = Rectangle(width=14.6, height=8.4, fill_color=color,
                   fill_opacity=1, stroke_width=0)
    label = Text(text, font=FONT, weight="BOLD", font_size=76, color=INK)
    if label.width > 12.5:
        label.scale(12.5 / label.width)
    return VGroup(bg, label)


def stick_idle(pos=ORIGIN, height=2.2, color=INK):
    return StickFigure(height=height, color=color, base=pos)


def stick_walk(figure, target, run_time=2.0, steps=6):
    return WalkTo(figure, target, steps=steps, run_time=run_time)


def stick_run(figure, target, run_time=1.5, steps=10):
    return RunTo(figure, target, steps=steps, run_time=run_time)


def stick_point(figure, target):
    figure.point(target)
    return figure


def stick_think(figure, text):
    return figure.think_bubble(text)


def stick_group(n, center=ORIGIN, spacing=1.4, height=2.0,
                color=INK, seed=7):
    """Multitud de n monigotes con ligera variación (reproducible)."""
    rng = np.random.default_rng(seed)
    figs = VGroup()
    total = (n - 1) * spacing
    for i in range(n):
        h = height * float(rng.uniform(0.9, 1.1))
        f = StickFigure(height=h, color=color,
                        base=center + RIGHT * (i * spacing - total / 2))
        f.refresh(float(rng.uniform(-0.15, 0.15)), 0.0)
        figs.add(f)
    return figs


def callout(text, color=ORANGE, font_size=96):
    """Dato/cifra destacada con fondo."""
    label = Text(text, font=FONT, weight="BOLD",
                 font_size=font_size, color=WHITE)
    pad = 0.35
    bg = Rectangle(width=label.width + pad * 2,
                   height=label.height + pad * 2,
                   fill_color=color, fill_opacity=1, stroke_width=0)
    return VGroup(bg, label)


def arrow(start, end, color=INK, width=8):
    return Arrow(start, end, color=color, stroke_width=width,
                 buff=0.1, max_tip_length_to_length_ratio=0.2)


def red_accent(target, scale=1.25):
    """Círculo rojo de énfasis alrededor de `target` (Mobject o punto)."""
    circle = Circle(color=RED, stroke_width=10)
    if hasattr(target, "get_center"):
        circle.move_to(target.get_center())
        circle.scale(max(target.width, target.height) * scale / 2
                     / circle.radius if circle.radius else 1)
    else:
        circle.move_to(np.array(target, dtype=float))
        circle.scale(scale)
    # jitter leve para look dibujado a mano
    pts = circle.get_points()
    rng = np.random.default_rng(3)
    circle.set_points(pts + rng.normal(0, 0.02, pts.shape))
    return circle


def split_screen(left_text, right_text, divider_color=INK):
    """Dos ideas en contraste."""
    div = Line(UP * 3.6, DOWN * 3.6, color=divider_color, stroke_width=6)
    l = Text(left_text, font=FONT, font_size=44, color=INK)
    l.move_to(LEFT * 3.6)
    r = Text(right_text, font=FONT, font_size=44, color=INK)
    r.move_to(RIGHT * 3.6)
    return VGroup(div, l, r)


def clock_montage(radius=1.6, color=INK):
    """Reloj cuyas manecillas giran rápido. Devuelve (reloj, animación)."""
    face = Circle(radius=radius, color=color, stroke_width=8)
    ticks = VGroup()
    for k in range(12):
        a = k * 2 * np.pi / 12
        p1 = np.array([np.cos(a), np.sin(a), 0.0]) * radius * 0.88
        p2 = np.array([np.cos(a), np.sin(a), 0.0]) * radius * 0.98
        ticks.add(Line(p1, p2, color=color, stroke_width=5))
    hour = Line(ORIGIN, UP * radius * 0.5, color=color, stroke_width=10)
    minute = Line(ORIGIN, UP * radius * 0.8, color=RED, stroke_width=7)
    clock = VGroup(face, ticks, hour, minute)

    class _Spin(Animation):
        def __init__(self, m, turns=6, run_time=2.0, **kw):
            super().__init__(m, run_time=run_time, **kw)
            self.turns = turns

        def interpolate_mobject(self, alpha):
            # manecillas = submobjects 2 y 3
            for hand, speed in ((self.mobject[2], 1), (self.mobject[3], 12)):
                hand.restore()
                hand.rotate(-alpha * self.turns * 2 * np.pi * speed,
                            about_point=self.mobject.get_center())

    for hand in (hour, minute):
        hand.save_state()
    return clock, _Spin(clock)


# ---------------------------------------------------------------- props (STORYBOARD.md)
def sol(color=YELLOW, radius=0.7, pos=ORIGIN):
    """Sol simple: círculo relleno + 8 rayos."""
    c = Circle(radius=radius, color=color, stroke_width=8,
               fill_color=color, fill_opacity=1)
    rays = VGroup()
    for k in range(8):
        a = k * PI / 4 + PI / 8
        d = np.array([np.cos(a), np.sin(a), 0.0])
        rays.add(Line(d * radius * 1.3, d * radius * 1.65,
                      color=color, stroke_width=8))
    g = VGroup(c, rays)
    g.move_to(np.array(pos, dtype=float))
    return g


def calendario(pos=ORIGIN, width=2.0):
    """Calendario de pared: marco + franja superior + líneas."""
    outer = Rectangle(width=width, height=width * 1.25, color=INK,
                      stroke_width=6, fill_color=WHITE, fill_opacity=1)
    top = Rectangle(width=width, height=width * 0.22, color=INK,
                    stroke_width=6, fill_color=INK, fill_opacity=1)
    top.move_to(outer.get_top() + DOWN * width * 0.11)
    lines = VGroup()
    for i in range(3):
        y = outer.get_center()[1] + width * 0.18 - i * width * 0.22
        lines.add(Line(LEFT * width * 0.32 + UP * y,
                       RIGHT * width * 0.32 + UP * y,
                       color=INK, stroke_width=4))
    g = VGroup(outer, top, lines)
    g.move_to(np.array(pos, dtype=float))
    return g


def pagina_calendario(width=1.7):
    """Hoja suelta para animar (cae / vuela)."""
    return Rectangle(width=width, height=width * 1.25, color=INK,
                     stroke_width=5, fill_color=WHITE, fill_opacity=1)


def reloj_pared(radius=1.0, pos=ORIGIN, hora_3=True):
    """Reloj de pared con manecillas fijas (las 3:00 por defecto)."""
    face = Circle(radius=radius, color=INK, stroke_width=8,
                  fill_color=WHITE, fill_opacity=1)
    ticks = VGroup()
    for k in range(12):
        a = k * 2 * np.pi / 12
        d = np.array([np.cos(a), np.sin(a), 0.0])
        ticks.add(Line(d * radius * 0.85, d * radius * 0.95,
                       color=INK, stroke_width=4))
    c = np.array(pos, dtype=float)
    hour = Line(ORIGIN, RIGHT * radius * 0.5, color=INK, stroke_width=8)
    minute = Line(ORIGIN, UP * radius * 0.75, color=INK, stroke_width=6)
    g = VGroup(face, ticks, hour, minute)
    g.move_to(c)
    return g


def pastel(pos=ORIGIN, width=1.8):
    """Pastel con 3 velas encendidas."""
    base = Rectangle(width=width, height=width * 0.45, color=INK,
                     stroke_width=6, fill_color=YELLOW, fill_opacity=1)
    velas = VGroup()
    for i, dx in enumerate((-width * 0.25, 0, width * 0.25)):
        vela = Line(UP * 0, UP * width * 0.3, color=INK, stroke_width=6)
        vela.move_to(np.array([dx, 0, 0]))
        flama = Circle(radius=width * 0.045, color=ORANGE, stroke_width=0,
                       fill_color=ORANGE, fill_opacity=1)
        flama.move_to(np.array([dx, width * 0.3 / 2 + width * 0.05, 0]))
        velas.add(vela, flama)
    velas.move_to(np.array([0, width * 0.225 + width * 0.15, 0]))
    g = VGroup(base, velas)
    g.move_to(np.array(pos, dtype=float))
    return g


def red_seguridad(width=4.5, height=0.7, pos=ORIGIN):
    """Red: cuadrícula de líneas."""
    g = VGroup()
    for i in range(9):
        x = -width / 2 + i * width / 8
        g.add(Line(np.array([x, -height / 2, 0]), np.array([x, height / 2, 0]),
                   color=INK, stroke_width=3))
    for j in range(3):
        y = -height / 2 + j * height / 2
        g.add(Line(np.array([-width / 2, y, 0]), np.array([width / 2, y, 0]),
                   color=INK, stroke_width=3))
    g.move_to(np.array(pos, dtype=float))
    return g


def caja(etiqueta, pos=ORIGIN, width=1.5):
    """Caja con etiqueta de texto."""
    rect = Rectangle(width=width, height=width * 0.7, color=INK,
                     stroke_width=6, fill_color=WHITE, fill_opacity=1)
    label = Text(etiqueta, font=FONT, font_size=26, color=INK)
    if label.width > width * 0.85:
        label.scale((width * 0.85) / label.width)
    g = VGroup(rect, label)
    g.move_to(np.array(pos, dtype=float))
    return g


def camino(width=7.0, pos=ORIGIN):
    """Camino curvo punteado."""
    func = ParametricFunction(
        lambda t: np.array([t, 0.45 * np.sin(t * 1.4), 0.0]),
        t_range=[-width / 2, width / 2, 0.05],
        color=INK, stroke_width=7)
    dashed = DashedVMobject(func, num_dashes=22, dashed_ratio=0.6)
    dashed.move_to(np.array(pos, dtype=float))
    return dashed


def casa(pos=ORIGIN, size=1.6):
    """Casa simple: cuadrado + techo."""
    body = Rectangle(width=size, height=size * 0.8, color=INK,
                     stroke_width=6, fill_color=WHITE, fill_opacity=1)
    roof = VGroup(
        Line(body.get_top() + LEFT * size * 0.55,
             body.get_top() + UP * size * 0.45, color=INK, stroke_width=6),
        Line(body.get_top() + UP * size * 0.45,
             body.get_top() + RIGHT * size * 0.55, color=INK, stroke_width=6))
    g = VGroup(body, roof)
    g.move_to(np.array(pos, dtype=float))
    return g


def oficina(pos=ORIGIN, size=1.6):
    """Oficina: rectángulo alto con ventanas."""
    body = Rectangle(width=size * 0.9, height=size * 1.3, color=INK,
                     stroke_width=6, fill_color=WHITE, fill_opacity=1)
    wins = VGroup()
    for i in range(2):
        for j in range(3):
            w = Rectangle(width=size * 0.18, height=size * 0.18, color=INK,
                          stroke_width=4)
            w.move_to(body.get_center() + np.array(
                [(j - 1) * size * 0.28, (0.5 - i) * size * 0.35, 0]))
            wins.add(w)
    g = VGroup(body, wins)
    g.move_to(np.array(pos, dtype=float))
    return g


def digitos(pos=ORIGIN, size=0.9):
    """Dígito grande para parpadear (la escena lo actualiza)."""
    t = Text("8", font=FONT, weight="BOLD", font_size=int(size * 72),
             color=INK)
    t.move_to(np.array(pos, dtype=float))
    return t


# ================================================================ RIG v2
# Caras expresivas, fondos y props con color (referencia: miniaturas y
# escenas del canal Zenn — personajes con gesto, elementos definidos).
from manim import Arc, Dot, Polygon, RoundedRectangle

EXPRESIONES = ("normal", "feliz", "preocupado", "sorpresa", "triste",
               "miedo", "dormido")


def expresion(fig, tipo="normal"):
    """Cara expresiva sobre la cabeza de un StickFigure. Devuelve VGroup.

    Añádela DESPUÉS de posicionar al monigote y no lo muevas después
    (la cara queda en coordenadas del mundo).
    """
    b, h = fig._base, fig.fig_height
    r = h * 0.13
    c = b + np.array([0.0, h - r, 0.0])
    col = fig.color
    parts = []
    er = r * 0.15
    for sx in (-1, 1):
        ex = c + np.array([sx * r * 0.38, r * 0.10, 0.0])
        if tipo == "dormido":
            parts.append(Line(ex + LEFT * er, ex + RIGHT * er,
                              color=col, stroke_width=5))
        elif tipo in ("sorpresa", "miedo"):
            parts.append(Circle(radius=er * 1.3, color=col, stroke_width=5)
                         .move_to(ex))
            parts.append(Dot(point=ex, radius=er * 0.45, color=col))
        else:
            parts.append(Dot(point=ex, radius=er * 0.9, color=col))
        by = c + np.array([sx * r * 0.38, r * 0.52, 0.0])
        if tipo in ("preocupado", "miedo"):
            parts.append(Line(by + np.array([-er, -er * 0.4, 0]),
                              by + np.array([er, er * 0.6, 0]),
                              color=col, stroke_width=5))
        elif tipo == "sorpresa":
            parts.append(Line(by + np.array([-er, er * 0.5, 0]),
                              by + np.array([er, er * 0.5, 0]),
                              color=col, stroke_width=5))
        elif tipo == "feliz":
            parts.append(Arc(radius=er * 1.1, start_angle=0.15 * PI,
                             angle=0.7 * PI, color=col, stroke_width=5)
                         .move_to(by))
        else:
            parts.append(Line(by + LEFT * er, by + RIGHT * er,
                              color=col, stroke_width=5))
    my = c + np.array([0.0, -r * 0.42, 0.0])
    if tipo == "feliz":
        parts.append(Arc(radius=r * 0.40, start_angle=PI, angle=PI,
                         color=col, stroke_width=6).move_to(my + UP * r * 0.1))
    elif tipo == "triste":
        parts.append(Arc(radius=r * 0.36, start_angle=0, angle=PI,
                         color=col, stroke_width=6).move_to(my - UP * r * 0.1))
    elif tipo in ("sorpresa", "miedo"):
        parts.append(Circle(radius=r * 0.16, color=col, stroke_width=6)
                     .move_to(my))
    elif tipo == "dormido":
        parts.append(Line(my + LEFT * r * 0.2, my + RIGHT * r * 0.2,
                          color=col, stroke_width=5))
    else:
        parts.append(Line(my + LEFT * r * 0.25, my + RIGHT * r * 0.25,
                          color=col, stroke_width=6))
    return VGroup(*parts)


def fondo(color=INK):
    """Rectángulo de fondo a pantalla completa (noches, espacio)."""
    return Rectangle(width=14.3, height=8.1, color=color,
                     fill_color=color, fill_opacity=1, stroke_width=0)


def estrellas(n=42, seed=7, color=WHITE):
    rng = np.random.default_rng(seed)
    pts = rng.uniform([-6.8, -3.6], [6.8, 3.6], size=(n, 2))
    return VGroup(*[Dot(point=np.array([x, y, 0]), radius=0.035,
                        color=color) for x, y in pts])


def luna(pos=ORIGIN, radio=1.0, color=YELLOW, bg=INK):
    """Luna creciente: círculo lleno + círculo del color del fondo encima."""
    full = Circle(radius=radio, color=color, fill_color=color,
                  fill_opacity=1, stroke_width=0)
    cut = Circle(radius=radio * 0.86, color=bg, fill_color=bg,
                 fill_opacity=1, stroke_width=0).shift(RIGHT * radio * 0.42
                                                        + UP * radio * 0.18)
    return VGroup(full, cut).move_to(pos)


def perro(pos=ORIGIN, color="#C98A4B", escala=1.0):
    """Perro de caricatura: cuerpo, cabeza, oreja, cola y patas."""
    body = Ellipse(width=1.7, height=1.05, color=INK, fill_color=color,
                   fill_opacity=1, stroke_width=6)
    head = Circle(radius=0.46, color=INK, fill_color=color, fill_opacity=1,
                  stroke_width=6).shift(RIGHT * 0.95 + UP * 0.42)
    ear = Ellipse(width=0.34, height=0.62, color=INK, fill_color="#8A5A2B",
                  fill_opacity=1, stroke_width=5).shift(RIGHT * 0.78
                                                        + UP * 0.62)
    snout = Ellipse(width=0.5, height=0.34, color=INK, fill_color=color,
                    fill_opacity=1, stroke_width=5).shift(RIGHT * 1.32
                                                          + UP * 0.30)
    nose = Dot(point=RIGHT * 1.55 + UP * 0.34, radius=0.07, color=INK)
    eye = Dot(point=RIGHT * 1.02 + UP * 0.52, radius=0.06, color=INK)
    tail = Arc(radius=0.5, start_angle=-0.5, angle=2.1, color=INK,
               stroke_width=9).shift(LEFT * 1.0 + UP * 0.35)
    legs = VGroup(*[Line(np.array([x, -0.35, 0]), np.array([x, -0.95, 0]),
                         color=INK, stroke_width=9)
                    for x in (-0.55, -0.22, 0.38, 0.65)])
    g = VGroup(body, tail, head, ear, snout, nose, eye, legs)
    return g.scale(escala).move_to(pos)


def gato(pos=ORIGIN, color="#F2A541", escala=1.0):
    """Gato de caricatura sentado: cuerpo, orejas triangulares, bigotes."""
    body = Ellipse(width=1.15, height=1.3, color=INK, fill_color=color,
                   fill_opacity=1, stroke_width=6)
    head = Circle(radius=0.52, color=INK, fill_color=color, fill_opacity=1,
                  stroke_width=6).shift(UP * 0.95)
    ears = VGroup(
        Polygon([-0.48, 1.28, 0], [-0.14, 1.32, 0], [-0.42, 1.72, 0],
                color=INK, fill_color=color, fill_opacity=1, stroke_width=5),
        Polygon([0.48, 1.28, 0], [0.14, 1.32, 0], [0.42, 1.72, 0],
                color=INK, fill_color=color, fill_opacity=1, stroke_width=5))
    eyes = VGroup(Dot(point=LEFT * 0.2 + UP * 1.0, radius=0.055, color=INK),
                  Dot(point=RIGHT * 0.2 + UP * 1.0, radius=0.055, color=INK))
    nose = Dot(point=UP * 0.86, radius=0.05, color=RED)
    whisk = VGroup(*[Line(np.array([sx * 0.25, 0.84 + dy, 0]),
                          np.array([sx * 0.72, 0.84 + dy * 1.6, 0]),
                          color=INK, stroke_width=3)
                     for sx in (-1, 1) for dy in (-0.07, 0.05)])
    tail = Arc(radius=0.55, start_angle=-1.2, angle=2.0, color=INK,
               stroke_width=9).shift(RIGHT * 0.72 - UP * 0.42)
    g = VGroup(tail, body, ears, head, eyes, nose, whisk)
    return g.scale(escala).move_to(pos)


def dino(pos=ORIGIN, color=TEAL, escala=1.0):
    """Dinosaurio de caricatura (perfil): cuerpo, cola, cabeza con dientes."""
    body = Ellipse(width=2.3, height=1.5, color=INK, fill_color=color,
                   fill_opacity=1, stroke_width=7)
    tail = Polygon([-0.7, 0.15, 0], [-2.2, 0.8, 0], [-0.75, -0.5, 0],
                   color=INK, fill_color=color, fill_opacity=1, stroke_width=6)
    head = RoundedRectangle(width=1.25, height=0.78, corner_radius=0.22,
                            color=INK, fill_color=color, fill_opacity=1,
                            stroke_width=7).shift(RIGHT * 1.45 + UP * 0.72)
    jaw = RoundedRectangle(width=1.05, height=0.3, corner_radius=0.12,
                           color=INK, fill_color=color, fill_opacity=1,
                           stroke_width=6).shift(RIGHT * 1.5 + UP * 0.22)
    teeth = VGroup(*[Polygon([1.05 + i * 0.22, 0.36, 0],
                             [1.16 + i * 0.22, 0.36, 0],
                             [1.10 + i * 0.22, 0.16, 0],
                             color=INK, fill_color=WHITE, fill_opacity=1,
                             stroke_width=2) for i in range(4)])
    eye = Dot(point=RIGHT * 1.28 + UP * 0.86, radius=0.07, color=INK)
    legs = VGroup(*[Line(np.array([x, -0.55, 0]), np.array([x, -1.3, 0]),
                         color=INK, stroke_width=11)
                    for x in (-0.55, 0.55)])
    arm = Line(np.array([0.85, 0.05, 0]), np.array([1.15, -0.25, 0]),
               color=INK, stroke_width=7)
    g = VGroup(tail, body, head, jaw, teeth, eye, arm, legs)
    return g.scale(escala).move_to(pos)


def fuego(pos=ORIGIN, escala=1.0):
    """Llamas en tres capas (roja, naranja, amarilla)."""
    def flame(w, h, col, dx=0.0):
        return Ellipse(width=w, height=h, color=col, fill_color=col,
                       fill_opacity=1, stroke_width=0).shift(RIGHT * dx)
    g = VGroup(flame(1.05, 1.6, RED, -0.18), flame(0.95, 1.45, RED, 0.3),
               flame(0.78, 1.2, ORANGE, 0.02), flame(0.45, 0.75, YELLOW, 0.05))
    return g.scale(escala).move_to(pos)


def lapida(texto="RIP", pos=ORIGIN, ancho=1.7):
    """Lápida gris con inscripción y hierba en la base."""
    stone = RoundedRectangle(width=ancho, height=ancho * 1.25,
                             corner_radius=ancho * 0.45, color=INK,
                             fill_color="#B9BEC7", fill_opacity=1,
                             stroke_width=7)
    label = Text(texto, font=FONT, font_size=44, color=INK)
    if label.width > ancho * 0.8:
        label.scale(ancho * 0.8 / label.width)
    label.move_to(stone.get_center() + UP * 0.15)
    base = Line(LEFT * ancho * 0.75, RIGHT * ancho * 0.75, color=INK,
                stroke_width=8).shift(DOWN * ancho * 0.66)
    grass = VGroup(*[Line(np.array([x, -ancho * 0.66, 0]),
                          np.array([x + 0.06, -ancho * 0.44, 0]),
                          color=TEAL, stroke_width=5)
                     for x in np.linspace(-ancho * 0.6, ancho * 0.6, 5)])
    return VGroup(stone, label, base, grass).move_to(pos)


def curva(pos=ORIGIN, ancho=5.2, alto=2.8, color=INK, acento=RED):
    """Curva tipo campana con punto rojo y flecha (gráficos de datos)."""
    curve = ParametricFunction(
        lambda t: np.array([t, alto * np.exp(-(t ** 2) / 3.2), 0]),
        t_range=np.array([-ancho / 2, ancho / 2, 0.05]),
        color=color, stroke_width=9)
    dot = Dot(point=np.array([0, alto, 0]), radius=0.16, color=acento)
    arr = Arrow(start=np.array([0.7, alto + 1.0, 0]),
                end=np.array([0.12, alto + 0.22, 0]), color=acento,
                stroke_width=8, buff=0.05)
    return VGroup(curve, dot, arr).move_to(pos)


def planeta(pos=ORIGIN, radio=0.95, color=TEAL):
    """Planeta con anillo (tipo Saturno)."""
    body = Circle(radius=radio, color=INK, fill_color=color, fill_opacity=1,
                  stroke_width=7)
    ring = Ellipse(width=radio * 3.1, height=radio * 0.85, color=ORANGE,
                   stroke_width=9)
    return VGroup(ring, body, ring.copy()).move_to(pos)


def casco_vikingo(pos=ORIGIN, escala=1.0):
    """Casco con cuernos (para escenas de historia/vikingos)."""
    dome = Arc(radius=0.75, start_angle=0, angle=PI, color=INK,
               stroke_width=10)
    dome_fill = Ellipse(width=1.5, height=0.75, color=INK,
                        fill_color="#9AA3AD", fill_opacity=1, stroke_width=0
                        ).shift(UP * 0.0)
    band = Rectangle(width=1.62, height=0.22, color=INK, fill_color="#6E767F",
                     fill_opacity=1, stroke_width=5).shift(DOWN * 0.02)
    horns = VGroup(
        Arc(radius=0.5, start_angle=0.3, angle=1.9, color=INK, stroke_width=8
            ).shift(LEFT * 0.78 + UP * 0.18),
        Arc(radius=0.5, start_angle=PI - 2.2, angle=1.9, color=INK,
            stroke_width=8).shift(RIGHT * 0.78 + UP * 0.18))
    g = VGroup(dome_fill, horns, dome, band)
    return g.scale(escala).move_to(pos)


def hueso(pos=ORIGIN, escala=1.0, color=WHITE):
    """Hueso de caricatura (premio del perro, fósiles)."""
    bar = Rectangle(width=1.5, height=0.42, color=INK, fill_color=color,
                    fill_opacity=1, stroke_width=6)
    knobs = VGroup(*[Circle(radius=0.30, color=INK, fill_color=color,
                            fill_opacity=1, stroke_width=6).shift(
                                np.array([sx * 0.78, sy * 0.22, 0]))
                     for sx in (-1, 1) for sy in (-1, 1)])
    return VGroup(bar, knobs).scale(escala).move_to(pos)


def vela(pos=ORIGIN, escala=1.0):
    """Vela encendida con llama y resplandor (escenas nocturnas)."""
    glow = Circle(radius=0.55, color=YELLOW, fill_color=YELLOW,
                  fill_opacity=0.25, stroke_width=0).shift(UP * 0.95)
    body = Rectangle(width=0.55, height=1.15, color=INK, fill_color=WHITE,
                     fill_opacity=1, stroke_width=6)
    flame = Ellipse(width=0.30, height=0.52, color=ORANGE, fill_color=ORANGE,
                    fill_opacity=1, stroke_width=0).shift(UP * 0.92)
    core = Ellipse(width=0.14, height=0.28, color=YELLOW, fill_color=YELLOW,
                   fill_opacity=1, stroke_width=0).shift(UP * 0.86)
    return VGroup(glow, body, flame, core).scale(escala).move_to(pos)


def moneda_dorada(texto="$", pos=ORIGIN, radio=0.8):
    """Moneda dorada grande con símbolo (dinero, historia)."""
    c = Circle(radius=radio, color=INK, fill_color="#FFC700",
               fill_opacity=1, stroke_width=8)
    inner = Circle(radius=radio * 0.74, color=INK, stroke_width=4)
    label = Text(texto, font=FONT, font_size=int(radio * 110), color=INK)
    return VGroup(c, inner, label).move_to(pos)


# ================================================================ RIG v3
# Zonas seguras + texto auto-ajustado + estilo ilustrado (Memorias de Pez).
# La cámara mide 14.22 x 8 (x: -7.1..7.1, y: -4..4).
# Los subtítulos quemados ocupan y < -2.4: NADA de texto ni elementos
# importantes debe ir ahí. Los helpers de texto de esta sección lo
# garantizan por construcción (auto-escala y tope de posición).

# Paleta ilustrada (mostaza, coral, azul marino, crema)
MOSTAZA = "#E8A838"
CORAL = "#E76F51"
AZUL_MARINO = "#1D3557"
CREMA = "#F4F1DE"

ZONA_TITULO_Y = 2.55    # altura estándar de bandas/títulos
ZONA_TEXTO_MIN_Y = -2.2  # ningún texto debajo de aquí (subtítulos)
ANCHO_SEGURO = 12.6     # x: -6.3 .. 6.3


def _ajustar(t, ancho_max):
    """Reduce el texto si excede el ancho máximo (nunca se sale)."""
    if t.width > ancho_max > 0:
        t.scale(ancho_max / t.width)
    return t


def banda_titulo(texto, color=ORANGE, y=ZONA_TITULO_Y, ancho_max=ANCHO_SEGURO):
    """Banda de título a lo ancho con texto auto-ajustado.

    Aunque el texto sea largo, se encoge solo: nunca se corta en los
    bordes. Úsala para los títulos de sección/capítulo.
    """
    label = _ajustar(Text(texto, font=FONT, font_size=72, color=WHITE),
                     ancho_max - 1.4)
    banda = Rectangle(width=ancho_max + 0.6, height=label.height + 0.75,
                      color=color, fill_color=color, fill_opacity=1,
                      stroke_width=0)
    return VGroup(banda, label).move_to(np.array([0.0, y, 0.0]))


def titulo_seguro(texto, color=INK, font_size=64, y=ZONA_TITULO_Y,
                  ancho_max=ANCHO_SEGURO):
    """Texto de título que nunca se sale del encuadre (auto-escala)."""
    t = _ajustar(Text(texto, font=FONT, font_size=font_size, color=color),
                 ancho_max)
    return t.move_to(np.array([0.0, y, 0.0]))


def etiqueta(texto, pos, color=INK, font_size=40, ancho_max=5.5):
    """Etiqueta pequeña auto-ajustada. `pos` = (x, y).

    Si pides una y muy baja, se sube sola para no invadir subtítulos.
    """
    t = _ajustar(Text(texto, font=FONT, font_size=font_size, color=color),
                 ancho_max)
    x, y = float(pos[0]), max(float(pos[1]), ZONA_TEXTO_MIN_Y + 0.35)
    return t.move_to(np.array([x, y, 0.0]))


def tarjeta_canal(texto="EL PORQUÉ", subtitulo="curiosidad científica"):
    """Tarjeta de apertura/cierre del canal (intro y despedida)."""
    bg = fondo(AZUL_MARINO)
    t1 = _ajustar(Text(texto, font=FONT, font_size=120, color=WHITE), 11.0)
    t1.move_to(UP * 0.5)
    t2 = Text(subtitulo, font=FONT, font_size=44, color=MOSTAZA)
    t2.next_to(t1, DOWN, buff=0.35)
    return VGroup(bg, t1, t2)


def personaje(pos=ORIGIN, cuerpo=TEAL, altura=2.6, expresion_tipo="feliz"):
    """Personaje ilustrado: cuerpo de color + cabeza con cara.

    Más 'dibujo' que el monigote de palitos, misma simplicidad.
    expresion_tipo: normal, feliz, preocupado, sorpresa, triste, miedo.
    """
    h = altura
    torso = RoundedRectangle(width=h * 0.42, height=h * 0.42,
                             corner_radius=h * 0.16, color=INK,
                             fill_color=cuerpo, fill_opacity=1,
                             stroke_width=7)
    torso.move_to(np.array([pos[0], pos[1] + h * 0.32, 0.0]))
    head_r = h * 0.14
    head = Circle(radius=head_r, color=INK, stroke_width=7)
    head.move_to(np.array([pos[0], pos[1] + h * 0.32 + h * 0.21
                           + head_r + 0.06, 0.0]))
    piernas = VGroup(*[
        Line(np.array([pos[0] + sx * h * 0.10, pos[1] + h * 0.12, 0.0]),
             np.array([pos[0] + sx * h * 0.13, pos[1], 0.0]),
             color=INK, stroke_width=8) for sx in (-1, 1)])
    brazos = VGroup(*[
        Line(np.array([pos[0] + sx * h * 0.20, pos[1] + h * 0.42, 0.0]),
             np.array([pos[0] + sx * h * 0.30, pos[1] + h * 0.20, 0.0]),
             color=INK, stroke_width=7) for sx in (-1, 1)])
    hc = head.get_center()
    er = head_r * 0.16
    ojos = VGroup(*[Dot(point=hc + np.array([sx * head_r * 0.36,
                                             head_r * 0.10, 0.0]),
                        radius=er * 0.95, color=INK) for sx in (-1, 1)])
    my = hc + np.array([0.0, -head_r * 0.38, 0.0])
    if expresion_tipo == "feliz":
        boca = Arc(radius=head_r * 0.42, start_angle=PI, angle=PI,
                   color=INK, stroke_width=6).move_to(my + UP * head_r * 0.1)
    elif expresion_tipo == "triste":
        boca = Arc(radius=head_r * 0.38, start_angle=0, angle=PI,
                   color=INK, stroke_width=6).move_to(my - UP * head_r * 0.1)
    elif expresion_tipo in ("sorpresa", "miedo"):
        boca = Circle(radius=head_r * 0.17, color=INK,
                      stroke_width=6).move_to(my)
    else:
        boca = Line(my + LEFT * head_r * 0.26, my + RIGHT * head_r * 0.26,
                    color=INK, stroke_width=6)
    return VGroup(piernas, torso, brazos, head, ojos, boca)


def pez(pos=ORIGIN, color=CORAL, escala=1.0):
    """Pez de dibujos: cuerpo, cola triangular, aleta y ojo."""
    body = Ellipse(width=1.9, height=1.0, color=INK, fill_color=color,
                   fill_opacity=1, stroke_width=6)
    tail = Polygon([-0.95, 0.0, 0], [-1.75, 0.55, 0], [-1.75, -0.55, 0],
                   color=INK, fill_color=color, fill_opacity=1, stroke_width=6)
    fin = Polygon([-0.1, 0.45, 0], [0.35, 0.95, 0], [0.45, 0.40, 0],
                  color=INK, fill_color=color, fill_opacity=1, stroke_width=5)
    eye_w = Circle(radius=0.16, color=INK, fill_color=WHITE, fill_opacity=1,
                   stroke_width=4).shift(RIGHT * 0.55 + UP * 0.15)
    eye_b = Dot(point=RIGHT * 0.58 + UP * 0.15, radius=0.07, color=INK)
    gill = Arc(radius=0.28, start_angle=-0.9, angle=1.8, color=INK,
               stroke_width=4).shift(RIGHT * 0.25)
    g = VGroup(tail, body, fin, eye_w, eye_b, gill)
    return g.scale(escala).move_to(pos)


def matraz(pos=ORIGIN, escala=1.0, liquido=TEAL):
    """Matraz de laboratorio con líquido de color y burbujas."""
    body = Polygon([-0.85, -0.7, 0], [0.85, -0.7, 0], [0.28, 0.75, 0],
                   [-0.28, 0.75, 0], color=INK, stroke_width=8,
                   fill_opacity=0)
    neck = Rectangle(width=0.56, height=0.5, color=INK, stroke_width=8,
                     fill_opacity=0).shift(UP * 0.95)
    liq = Polygon([-0.68, -0.58, 0], [0.68, -0.58, 0], [0.30, 0.30, 0],
                  [-0.30, 0.30, 0], color=liquido, fill_color=liquido,
                  fill_opacity=1, stroke_width=0)
    bubbles = VGroup(*[Circle(radius=0.07, color=WHITE, stroke_width=4)
                       .shift(np.array([bx, by, 0.0]))
                       for bx, by in ((-0.25, -0.15), (0.1, 0.05),
                                      (0.35, -0.3))])
    g = VGroup(liq, bubbles, body, neck)
    return g.scale(escala).move_to(pos)


def ojo_grande(pos=ORIGIN, escala=1.0, iris=TEAL):
    """Ojo grande de dibujos (observar, descubrir, vigilar)."""
    white = Ellipse(width=2.2, height=1.25, color=INK, fill_color=WHITE,
                    fill_opacity=1, stroke_width=7)
    iris_c = Circle(radius=0.34, color=INK, fill_color=iris, fill_opacity=1,
                    stroke_width=5)
    pupil = Dot(radius=0.15, color=INK)
    shine = Dot(point=UP * 0.12 + LEFT * 0.1, radius=0.07, color=WHITE)
    g = VGroup(white, iris_c, pupil, shine)
    return g.scale(escala).move_to(pos)
