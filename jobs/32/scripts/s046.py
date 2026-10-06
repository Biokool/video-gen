from manim import *
from zenn_rig import *

class S046(Scene):
    def construct(self):
        prota = protagonista(pos=ORIGIN, playera=PLAYERA_AMARILLA, altura=2.6, expresion='pensando', pose='de_pie')
        trophy = moneda_dorada(texto='$', pos=RIGHT*2+UP*0.5, radio=0.8)
        limit_bar = red_seguridad(width=4.5, height=0.7, pos=LEFT*2+DOWN*0.5)

        self.play(FadeIn(prota), run_time=1)
        self.play(FadeIn(trophy), run_time=1)
        self.play(Create(limit_bar), run_time=1)
        self.wait(0.5)
        self.play(prota.animate.shift(RIGHT*0.3), run_time=0.5)
        self.play(prota.animate.shift(LEFT*0.6), run_time=0.5)
        self.play(prota.animate.shift(RIGHT*0.3), run_time=0.5)
        self.wait(1)