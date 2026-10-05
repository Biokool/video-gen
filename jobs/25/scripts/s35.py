from manim import *
from zenn_rig import *

class S35(Scene):
    def construct(self):
        pro = protagonista(
            LEFT * 3.5,
            playera="rosa",
            altura=3.0,
            expresion="sorpresa",
            pose="senalando"
        )
        ojo = ojo_grande(RIGHT * 1.8 + UP * 1.5, escala=1.1, iris=TEAL)
        patron = curva(RIGHT * 1.8 + DOWN * 0.8, ancho=3.8, alto=2.0, color=TEAL, acento=RED)

        self.play(FadeIn(pro), FadeIn(ojo), Create(patron), run_time=1.2)
        self.wait(0.8)
        cambiar_cara(pro, "feliz")
        self.play(pro.animate.shift(UP * 0.15), run_time=0.4)
        self.wait(1.1)
        self.play(FadeOut(pro), FadeOut(ojo), FadeOut(patron), run_time=0.5)
        self.wait(0.5)