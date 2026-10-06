from manim import *
from zenn_rig import *

class S034(Scene):
    def construct(self):
        prota = protagonista(pos=ORIGIN, playera='roja', altura=3.0, expresion='enojado', pose='de_pie')
        sun = sol(color=YELLOW, radius=0.7, pos=LEFT*3 + UP*2)
        ache = red_accent(prota, scale=1.25)

        self.play(FadeIn(prota), FadeIn(sun), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(ache), run_time=0.8)
        self.wait(1.5)
        self.play(sun.animate.shift(UP*0.5), run_time=1.0)
        self.wait(0.5)