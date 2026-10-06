from manim import *
from zenn_rig import *

class S020(Scene):
    def construct(self):
        prota = protagonista(
            pos=DOWN*1.2+LEFT*3.5,
            playera=PLAYERA_VERDE,
            altura=2.5,
            expresion='pensando',
            pose='de_pie'
        )
        sangre = curva(
            pos=RIGHT*2+UP*0.5,
            ancho=3.0,
            alto=1.0,
            color=RED,
            acento=RED
        )
        gota = moneda_dorada(
            texto='$',
            pos=RIGHT*2+UP*0.5,
            radio=0.2
        )

        self.play(FadeIn(prota), run_time=0.8)
        self.play(Create(sangre), run_time=0.8)
        self.play(FadeIn(gota), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(gota), run_time=0.5)
        self.wait(0.2)