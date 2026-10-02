from manim import *
from zenn_rig import *

class S06(Scene):
    def construct(self):
        # Black hole (solid dark circle) and its event‑horizon ring
        hole = Circle(radius=1.2, color=INK, fill_opacity=1).shift(2 * RIGHT)
        horizon = Circle(radius=1.4, color=WHITE, stroke_width=2).shift(2 * RIGHT)

        # Stick figure (already near the hole, ready to be spaghettified)
        stick = stick_idle(pos=LEFT * 2 + DOWN * 0.5, height=2.2, color=INK)

        # Short callout that will appear later
        note = callout("¡Spaghettificación!", color=ORANGE, font_size=96).next_to(stick, UP)

        # 1️⃣ Aparecen el agujero negro y el monigote
        self.play(FadeIn(hole), FadeIn(horizon), FadeIn(stick), run_time=2)
        self.wait(1)

        # 2️⃣ El monigote se estira (spaghettificación)
        elongated = stick.copy().stretch(3, 1)  # stretch vertically
        self.play(Transform(stick, elongated), run_time=1.5)
        self.wait(0.5)

        # 3️⃣ Se acerca lentamente al horizonte (ya elongado)
        target_pos = hole.get_center() + LEFT * 0.4
        self.play(stick_walk(stick, target_pos, run_time=2))
        self.wait(0.5)

        # 4️⃣ Aparece el callout breve
        self.play(FadeIn(note), run_time=1)
        self.wait(2)

        # 5️⃣ Giro lento del agujero negro para dar dinamismo
        self.play(
            Rotate(hole, angle=TAU, about_point=hole.get_center()),
            Rotate(horizon, angle=TAU, about_point=horizon.get_center()),
            run_time=4,
        )
        self.wait(1)

        # 6️⃣ Desvanecimiento final
        self.play(FadeOut(VGroup(hole, horizon, stick, note)), run_time=1.5)