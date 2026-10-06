from manim import *
from zenn_rig import *

class S027(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*2, playera=PLAYERA_VERDE, altura=3.0,
                             expresion='preocupado', pose='de_pie')
        gear = curva(pos=RIGHT*2, ancho=2.0, alto=2.0, color=INK, acento=RED)
        bar = red_seguridad(width=4.0, height=0.3, pos=DOWN*1.5)

        self.play(FadeIn(prota), FadeIn(gear), FadeIn(bar), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(prota), FadeOut(gear), FadeOut(bar), run_time=1.0)
        self.wait(0.5)