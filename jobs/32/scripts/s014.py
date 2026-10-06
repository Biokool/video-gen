from manim import *
from zenn_rig import *

class S014(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3.5, playera='azul', altura=2.6, expresion='sorpresa', pose='de_pie')
        flask = matraz(pos=RIGHT*3.5, escala=1.0, liquido=RED)
        label = callout(text="<500 ml", color=ORANGE, font_size=96)
        self.play(FadeIn(prota), run_time=1)
        self.play(Create(flask), run_time=1)
        self.play(FadeIn(label), run_time=1)
        self.wait(6)