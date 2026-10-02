from manim import *
from zenn_rig import *

class S04(Scene):
    def construct(self):
        # Posiciones
        earth_pos = LEFT * 4
        bh_pos = RIGHT * 4

        # Monigote en la Tierra
        stick = stick_idle(earth_pos, height=2.2, color=INK)
        self.play(FadeIn(stick, scale=0.5))
        self.wait(1)

        # Flechas de gravedad uniformes (misma longitud)
        foot = stick.get_bottom()
        uniform_arrow = arrow(foot, foot + DOWN * 1, color=RED)
        self.play(FadeIn(uniform_arrow, scale=0.5))
        self.wait(2)

        # Aproximación al agujero negro
        self.play(stick_walk(stick, bh_pos, run_time=5))
        self.wait(1)

        # Cambiar a flechas más largas en los pies
        self.play(FadeOut(uniform_arrow))
        new_foot = stick.get_bottom()
        strong_arrow = arrow(new_foot, new_foot + DOWN * 2.5, color=RED)
        self.play(FadeIn(strong_arrow, scale=0.5))
        self.wait(3)

        # Mantener escena final unos segundos
        self.wait(5)