from manim import *
from zenn_rig import *

class S49(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*2, playera=PLAYERA_NARANJA, altura=3.0, expresion='feliz', pose='de_pie')
        sol_obj = sol(color=YELLOW, radius=0.7, pos=LEFT*2+DOWN*1.5)
        self.play(FadeIn(prota), FadeIn(sol_obj))
        self.wait(0.5)
        cambiar_cara(prota, 'pensando')
        self.wait(0.5)
        txt = callout(text="¿Por qué el cielo es azul?", color=ORANGE, font_size=40, pos=RIGHT*3+UP*1)
        self.play(FadeIn(txt))
        self.wait(2.0)