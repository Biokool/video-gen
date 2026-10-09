from manim import *
from zenn_rig import *

class S52(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3.5 + DOWN*0.2, playera="naranja", altura=2.6, expresion="pensando", pose="de_pie")
        call = callout(text="art_vs_history", color=ORANGE, font_size=60, ancho_max=7.0, pos=RIGHT*3.4+UP*1)
        sun = sol(color=YELLOW, radius=0.7, pos=UP*2+LEFT*1)
        self.play(FadeIn(prota, call, sun), run_time=0.8)
        self.wait(1.6)