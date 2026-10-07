from manim import *
from zenn_rig import *

class S024(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*4 + DOWN*1, playera=PLAYERA_VERDE, altura=2.6, expresion='sorpresa', pose='de_pie')
        heart = curva(pos=RIGHT*2 + UP*0.5, ancho=3.0, alto=1.8, color=INK, acento=RED)
        oxy = etiqueta('O2', pos=heart.get_center(), color=INK, font_size=40, ancho_max=5.5)

        self.play(FadeIn(prota), FadeIn(heart), FadeIn(oxy))
        self.wait(0.5)

        for _ in range(5):
            self.play(heart.animate.scale(1.3), run_time=0.2)
            self.play(heart.animate.scale(1/1.3), run_time=0.2)

        self.play(Rotate(oxy, angle=TAU, about_point=heart.get_center(), run_time=3))
        self.wait(1)