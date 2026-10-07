from manim import *
from zenn_rig import *

class S04(Scene):
    def construct(self):
        prota = protagonista(pos=ORIGIN, playera=PLAYERA_NARANJA, altura=3.0, expresion='pensando', pose='de_pie')
        sol_obj = sol(color=YELLOW, radius=0.7, pos=UP*2)
        fuego_obj = fuego(pos=RIGHT*2+DOWN*0.5, escala=1.0)

        self.play(FadeIn(prota), FadeIn(sol_obj), FadeIn(fuego_obj), run_time=1.5)
        self.wait(2.5)
        self.play(FadeOut(prota), FadeOut(sol_obj), FadeOut(fuego_obj), run_time=1.0)