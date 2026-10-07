from manim import *
from zenn_rig import *

class S029(Scene):
    def construct(self):
        prota = protagonista(pos=ORIGIN, playera="verde", altura=2.6, expresion="pregunta", pose="de_pie")
        energia_caja = caja("20% energía", pos=LEFT*2 + UP*0.5)
        signo = etiqueta("?", pos=RIGHT*2 + UP*0.5)

        self.play(FadeIn(prota), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(energia_caja), FadeIn(signo), run_time=1.5)
        self.wait(2.0)
        self.play(prota.animate.shift(LEFT*0.3), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(energia_caja), FadeOut(signo), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(prota), run_time=1.0)