from manim import *
from zenn_rig import *

class S04(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT*3.5 + DOWN*1.2,
            playera=PLAYERA_NARANJA,
            altura=2.5,
            expresion='decidido',
            pose='de_pie'
        )
        sol_obj = sol(color=YELLOW, radius=0.9, pos=UP*2 + RIGHT*2)
        fuego_obj = fuego(pos=RIGHT*3.5 + DOWN*0.5, escala=1.0)
        callout_obj = callout(text="Obsesión", color=ORANGE, font_size=96).shift(UP*2)

        self.play(FadeIn(prota), Create(sol_obj), run_time=1.5)
        self.play(FadeIn(fuego_obj), Write(callout_obj), run_time=1.5)
        self.wait(1.0)