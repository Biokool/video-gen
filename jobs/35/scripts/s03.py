from manim import *
from zenn_rig import *

class S03(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_NARANJA, altura=2.6, expresion='euforico', pose='senalando')
        sun = sol(color=YELLOW, radius=0.7, pos=RIGHT*3.5)
        self.play(FadeIn(prota), FadeIn(sun), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(prota), FadeOut(sun), run_time=1.0)