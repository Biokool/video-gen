from manim import *
from zenn_rig import *

class S023(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera="verde", altura=2.6, expresion="decidido", pose="de_pie")
        heart = etiqueta("❤️", pos=RIGHT*2+UP*0.5, color=RED, font_size=40)
        weight = caja("peso", pos=RIGHT*2+DOWN*0.5)

        self.play(FadeIn(prota), FadeIn(heart), FadeIn(weight))
        self.play(heart.animate.scale(1.3), run_time=0.5)
        self.play(heart.animate.scale(1/1.3), run_time=0.5)
        self.wait(1.5)