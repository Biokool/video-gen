from manim import *
from zenn_rig import *

class S018(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera="verde", altura=2.6, expresion="pensando", pose="senalando")
        rio = curva(pos=ORIGIN, ancho=5.2, alto=2.8, color=INK, acento=RED)
        gota = planeta(pos=RIGHT*3.5+DOWN*0.5, radio=0.2, color=TEAL)

        self.play(FadeIn(prota), run_time=0.8)
        self.play(Create(rio), run_time=0.8)
        self.play(FadeIn(gota), run_time=0.8)
        self.wait(0.6)