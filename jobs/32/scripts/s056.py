from manim import *
from zenn_rig import *

class S056(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3 + DOWN*0.5, playera="teal", altura=2.6, expresion="feliz", pose="de_pie")
        ar = arrow(start=[-1,0,0], end=[1,0,0], color=INK, width=8)
        clock = reloj_pared(radius=1.0, pos=RIGHT*3 + DOWN*0.5, hora_3=True)

        self.play(FadeIn(prota), run_time=1)
        self.wait(0.5)
        self.play(Create(ar), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(clock), run_time=1)
        self.wait(1)