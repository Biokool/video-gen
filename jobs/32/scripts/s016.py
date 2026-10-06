from manim import *
from zenn_rig import *

class S016(Scene):
    def construct(self):
        prota = protagonista(pos=ORIGIN, playera=PLAYERA_AZUL, altura=2.6, expresion='pensando', pose='de_pie')
        grafica = curva(pos=RIGHT*2.5, ancho=5.2, alto=2.8, color=INK, acento=RED)
        etiqueta_estudio = etiqueta('Popkin et al., 2010, Nutrition Reviews', pos=(0, -1.8), color=INK, font_size=40, ancho_max=5.5)

        self.play(FadeIn(prota), run_time=1.0)
        self.wait(2.0)
        self.play(Create(grafica), run_time=1.5)
        self.wait(2.0)
        self.play(FadeIn(etiqueta_estudio), run_time=1.0)
        self.wait(4.0)
        self.wait(1.5)