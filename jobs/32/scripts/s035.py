from manim import *
from zenn_rig import *

class S035(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*2, playera="roja", altura=2.6, expresion="decidido", pose='de_pie')
        signo = etiqueta("=", (0,0), color=INK, font_size=40)
        estudio = matraz(pos=RIGHT*2, escala=1.0, liquido=TEAL)

        self.play(FadeIn(prota), run_time=0.5)
        self.play(FadeIn(signo), FadeIn(estudio), run_time=0.5)
        self.wait(1.0)