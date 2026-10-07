from manim import *
from zenn_rig import *

class S07(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*2 + DOWN*0.5, playera=PLAYERA_AZUL, altura=2.6, expresion='decidido', pose='de_pie')
        wave = curva(pos=RIGHT*2 + UP*0.5, ancho=3.0, alto=1.2, color=INK, acento=RED)
        drop = planeta(pos=RIGHT*3.5 + UP*0.5, radio=0.3, color=TEAL)

        self.play(FadeIn(prota), run_time=1.5)
        self.wait(0.5)
        self.play(Create(wave), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(drop), run_time=1.0)
        self.wait(0.5)
        self.play(wave.animate.scale(1.1), run_time=0.5)
        self.wait(0.2)
        self.play(wave.animate.scale(1/1.1), run_time=0.5)
        self.wait(1.0)