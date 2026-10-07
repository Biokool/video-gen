from manim import *
from zenn_rig import *

class S06(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3.5+DOWN*0.5, playera=PLAYERA_NARANJA, altura=2.2, expresion='sorprendido', pose='de_pie')
        cerebro = curva(pos=LEFT*1.0+UP*0.5, ancho=3.0, alto=1.5, color=INK, acento=RED)
        dato = callout(text="1%", color=ORANGE, pos=RIGHT*3.4+UP*1)

        self.play(FadeIn(prota), run_time=1.5)
        self.wait(0.5)
        self.play(Create(cerebro), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(dato), run_time=1.0)
        self.wait(1.0)