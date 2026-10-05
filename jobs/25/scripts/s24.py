from manim import *
from zenn_rig import *

class S24(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT * 4, playera="azul", expresion="sorpresa", pose="senalando")
        ojo = ojo_grande(pos=RIGHT * 4, escala=1.3, iris=TEAL)
        mat = matraz(pos=RIGHT * 1.2 + DOWN * 0.8, escala=0.7, liquido=TEAL)

        self.play(FadeIn(prota), run_time=0.7)
        self.play(FadeIn(ojo), FadeIn(mat), run_time=0.8)

        c = callout("¿Qué ves?", color=ORANGE, font_size=76)
        self.play(FadeIn(c), run_time=0.7)
        self.play(prota.animate.shift(UP * 0.4), ojo.animate.scale(1.1), run_time=0.7)
        self.wait(1.4)
        self.play(FadeOut(c), FadeOut(prota), FadeOut(ojo), FadeOut(mat), run_time=0.6)