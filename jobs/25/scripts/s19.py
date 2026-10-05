from manim import *
from zenn_rig import *

class S19(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT * 3.5 + DOWN * 1.0, playera="verde", altura=3.0, expresion='pensando', pose='senalando')
        curva_m = curva(pos=RIGHT * 3.0 + DOWN * 0.3, ancho=5.0, alto=2.6, acento=RED)
        ojo_m = ojo_grande(pos=RIGHT * 3.0 + UP * 2.8, escala=0.6)
        callout_m = callout("¡Punto óptimo!", color=GREEN, font_size=72)

        self.play(FadeIn(prota, shift=UP * 0.5), run_time=0.8)
        self.play(Create(curva_m), run_time=1.2)
        self.play(FadeIn(ojo_m), run_time=0.5)
        self.play(FadeIn(callout_m), run_time=0.5)
        self.wait(1.0)