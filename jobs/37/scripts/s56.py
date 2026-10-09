from manim import *
from zenn_rig import *

class S56(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3, playera=PLAYERA_NARANJA, altura=3.0, expresion='pensando', pose='senalando')
        casco = casco_vikingo(pos=RIGHT*3, escala=1.0)
        self.play(FadeIn(prota), run_time=1.0)
        self.play(FadeIn(casco), run_time=1.0)
        self.wait(4.0)