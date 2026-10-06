from manim import *
from zenn_rig import *

class S032(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera="roja", altura=2.6, expresion="pensando", pose="de_pie")
        mat = matraz(pos=ORIGIN, escala=1.0, liquido=TEAL)
        curv = curva(pos=DOWN*1.2+RIGHT*3.5, ancho=2.0, alto=1.5, color=INK, acento=RED)

        self.play(FadeIn(prota), run_time=1.5)
        self.play(FadeIn(mat), run_time=1.5)
        self.play(Create(curv), run_time=1.5)
        self.wait(1.0)
        self.play(Transform(prota, cambiar_cara(prota, "sorpresa")))
        self.wait(1.5)