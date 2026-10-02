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
