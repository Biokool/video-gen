from manim import *
from zenn_rig import *

class S019(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3+DOWN*0.5, playera=PLAYERA_VERDE, altura=2.6, expresion='pensando', pose='de_pie')
        rio = curva(pos=RIGHT*2, ancho=4.0, alto=0.8, color=INK, acento=RED)
        b1 = moneda_dorada(texto='$', pos=rio.get_center()+UP*0.3+LEFT*0.4, radio=0.2)
        b2 = moneda_dorada(texto='$', pos=rio.get_center()+UP*0.1+RIGHT*0.2, radio=0.2)
        b3 = moneda_dorada(texto='$', pos=rio.get_center()+DOWN*0.2+LEFT*0.1, radio=0.2)
        burbujas = VGroup(b1, b2, b3)

        self.play(FadeIn(prota), run_time=1.0)
        self.play(Create(rio), run_time=1.5)
        self.play(FadeIn(burbujas), run_time=1.0)
        self.wait(1.0)