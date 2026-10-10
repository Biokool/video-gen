from manim import *
from zenn_rig import *

class S54(Scene):
    def construct(self):
        prota = protagonista(pos=ORIGIN + DOWN*2.4, playera=PLAYERA_NARANJA, altura=3.0, expresion='feliz', pose='de_pie')
        sol_obj = sol(color=YELLOW, radius=0.7, pos=LEFT*4 + UP*1.5)
        txt = callout("¿Por qué el cielo es azul?", color=ORANGE, font_size=50, ancho_max=7.0, pos=RIGHT*3 + UP*2.2)

        self.play(FadeIn(prota), run_time=1.0)
        self.play(FadeIn(sol_obj), run_time=1.0)
        self.play(FadeIn(txt), run_time=1.0)
        self.wait(1.0)