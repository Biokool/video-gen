from manim import *
from zenn_rig import *

class S17(Scene):
    def construct(self):
        prota = protagonista(pos=(-4.0, -0.5, 0), playera="verde",
                             expresion="pensando", pose="de_pie")
        cur = curva(pos=(3.6, -0.9, 0), ancho=5.2, alto=2.8, color=INK, acento=RED)
        ojo = ojo_grande(pos=(4.5, 2.6, 0), escala=0.8, iris=TEAL)
        co = callout("ÓPTIMO: 2-6 m", color=ORANGE, font_size=72).move_to((-3.7, 3.0, 0))
        pie = etiqueta("cerebro + ojos", (-4.0, -1.9, 0), color=INK, font_size=36)

        self.play(FadeIn(prota), run_time=0.7)
        self.play(Create(cur), run_time=1.6)
        self.play(FadeIn(ojo), FadeIn(pie), run_time=0.7)

        prota2 = protagonista(pos=(-4.0, -0.5, 0), playera="verde",
                              expresion="alegria_pura", pose="senalando")
        self.play(Transform(prota, prota2), run_time=0.9)

        self.play(Write(co), run_time=1.0)
        self.wait(2.4)