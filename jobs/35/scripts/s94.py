from manim import *
from zenn_rig import *

class S94(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3.5+DOWN*1.2, playera=PLAYERA_NARANJA, altura=2.6, expresion='pensando', pose='de_pie')
        self.play(FadeIn(prota), run_time=1.0)
        self.wait(0.5)
        cf = callout("factores sociales, culturales o de aprendizaje", color=ORANGE, font_size=60, ancho_max=7.0, pos=RIGHT*3.4+UP*1)
        self.play(FadeIn(cf), run_time=1.0)
        self.wait(0.5)
        self.play(prota.animate.shift(RIGHT*0.3), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(cf), run_time=0.5)
        self.wait(0.5)