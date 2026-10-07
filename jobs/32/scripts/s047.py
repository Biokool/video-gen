from manim import *
from zenn_rig import *

class S047(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT*2 + DOWN*0.5,
            playera=PLAYERA_AMARILLA,
            altura=2.6,
            expresion='preocupado',
            pose='de_pie'
        )
        nota = callout(
            text="Deshidratación extrema → desequilibrio electrolítico (Na+, K+)",
            color=ORANGE,
            pos=RIGHT*3 + UP*1
        )
        señal = curva(
            pos=ORIGIN,
            ancho=3.0,
            alto=1.5,
            color=INK,
            acento=RED
        )

        self.play(FadeIn(prota), run_time=0.5)
        self.play(FadeIn(nota), run_time=0.5)
        self.play(Create(señal), run_time=1.0)
        self.wait(2.0)
        self.play(prota.animate.shift(RIGHT*0.3), run_time=0.5)
        self.play(prota.animate.shift(LEFT*0.3), run_time=0.5)
        self.wait(3.0)