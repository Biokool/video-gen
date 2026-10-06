from manim import *
from zenn_rig import *

class S022(Scene):
    def construct(self):
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_VERDE,
            altura=2.6,
            expresion='preocupado',
            pose='de_pie'
        )
        sangre = curva(
            pos=DOWN*1.2 + RIGHT*2,
            ancho=3.0,
            alto=1.5,
            color=INK,
            acento=RED
        )
        bomba = caja(
            etiqueta="Bomba",
            pos=UP*0.5,
            width=1.5
        )
        self.play(FadeIn(prota), run_time=1)
        self.play(Create(sangre), run_time=1)
        self.play(FadeIn(bomba), run_time=1)
        self.play(FadeIn(red_accent(bomba, scale=1.25)), run_time=0.5)
        self.wait(1.5)