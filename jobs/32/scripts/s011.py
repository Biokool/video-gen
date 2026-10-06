from manim import *
from zenn_rig import *

class S011(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*2 + DOWN*0.5, playera=PLAYERA_AZUL, altura=2.6, expresion='sorpresa', pose='de_pie')
        accent = red_accent(prota, scale=1.25)
        alert = callout(">300 mOsm/kg", color=RED, font_size=96)
        alert.move_to(RIGHT*2 + UP*0.5)

        self.play(FadeIn(prota), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(accent), run_time=0.5)
        self.play(FadeIn(alert), run_time=1.0)
        self.wait(6.0)