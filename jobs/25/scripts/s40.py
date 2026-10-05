from manim import *
from zenn_rig import *

class S40(Scene):
    def construct(self):
        self.add(fondo(INK))
        prota = version_prota(5, pos=LEFT * 4.5)
        self.play(FadeIn(prota, shift=UP), run_time=1.0)

        stick = stick_idle(pos=LEFT * 2, height=2.2, color=YELLOW)
        expresion(stick, "sorpresa")
        self.play(FadeIn(stick, shift=UP), run_time=1.0)

        eye = ojo_grande(pos=RIGHT * 3, escala=1.0, iris=YELLOW)
        self.play(FadeIn(eye, shift=LEFT), run_time=1.0)

        qmark = callout("¿?", color=ORANGE)
        qmark.next_to(stick.get_top(), UP, buff=0.3)
        self.play(FadeIn(qmark, scale=0.5), run_time=1.0)
        self.wait(1.5)
        self.play(qmark.animate.shift(UP * 0.2), run_time=0.5)
        self.wait(1.5)