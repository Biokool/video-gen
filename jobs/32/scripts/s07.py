from manim import *
from zenn_rig import *

class S07(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.5 + LEFT*2, playera=PLAYERA_AZUL, altura=3.0, expresion='feliz', pose='de_pie')
        wave = curva(pos=RIGHT*2 + UP*0.5, ancho=3.0, alto=1.0, color=TEAL, acento=RED)
        drop_box = caja(etiqueta="Gota", pos=RIGHT*2 + DOWN*0.5, width=1.5)
        sed_callout = callout(text="Sed", color=ORANGE, font_size=96).move_to(UP*2)

        self.play(FadeIn(prota), run_time=1.5)
        self.play(Create(wave), run_time=1.0)
        self.play(FadeIn(drop_box), run_time=0.8)
        self.play(FadeIn(sed_callout), run_time=0.8)
        self.wait(2)