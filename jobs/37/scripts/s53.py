from manim import *
from zenn_rig import *

class S53(Scene):
    def construct(self):
        title = title_card("LA FICCIÓN ES MÁS FUERTE QUE LA HISTORIA", color=YELLOW)
        self.play(FadeIn(title), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(title), run_time=1)

        prota = protagonista(pos=DOWN*1.2 + LEFT*3.5, playera="naranja", altura=2.2, expresion="pensando", pose="de_pie")
        sun = sol(color=YELLOW, radius=0.7, pos=RIGHT*3.5 + UP*1)

        self.play(FadeIn(prota), FadeIn(sun), run_time=1)
        self.wait(0.5)