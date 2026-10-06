from manim import *
from zenn_rig import *

class S023(Scene):
    def construct(self):
        prota = protagonista(pos=ORIGIN, playera=PLAYERA_VERDE, altura=3.0, expresion='decidido', pose='de_pie')
        heart = callout("❤", color=RED, font_size=96).shift(LEFT*2 + UP*1)
        weight = etiqueta("⚖️", pos=RIGHT*2 + UP*1, color=INK, font_size=40)

        self.play(FadeIn(prota), run_time=1)
        self.play(FadeIn(heart), FadeIn(weight), run_time=1)
        self.play(heart.animate.scale(1.2), run_time=0.5)
        self.play(heart.animate.scale(1/1.2), run_time=0.5)
        self.play(heart.animate.scale(1.2), run_time=0.5)
        self.play(heart.animate.scale(1/1.2), run_time=0.5)
        self.wait(0.5)