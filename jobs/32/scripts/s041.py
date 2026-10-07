from manim import *
from zenn_rig import *

class S041(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera="amarilla", altura=2.4, expresion="enfocado", pose="de_pie")
        cerebro = curva(pos=RIGHT*3.5+UP*1.0, ancho=2.5, alto=1.5, color=INK, acento=RED)
        celula = caja(etiqueta="escudo", pos=RIGHT*3.5+DOWN*1.0, width=1.5)

        self.play(FadeIn(prota), run_time=1)
        self.play(FadeIn(cerebro), run_time=1)
        self.play(FadeIn(celula), run_time=1)
        self.wait(2)