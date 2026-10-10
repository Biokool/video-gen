from manim import *
from zenn_rig import *

class S04(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*2, playera=PLAYERA_NARANJA, altura=2.6,
                             expresion='pensativo', pose='senalando')
        sol_obj = sol(color=YELLOW, radius=0.7, pos=RIGHT*3+DOWN*1)
        callout_obj = callout("¿Por qué usamos más una mano?", color=ORANGE,
                              pos=RIGHT*4+UP*1)
        self.play(FadeIn(prota), FadeIn(sol_obj), run_time=1.0)
        self.play(FadeIn(callout_obj), run_time=1.0)
        self.wait(2.0)