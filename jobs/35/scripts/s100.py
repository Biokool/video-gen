from manim import *
from zenn_rig import *

class S100(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*2, playera=PLAYERA_NARANJA, altura=2.6, expresion='normal', pose='de_pie')
        cambiar_cara(prota, "pensando")
        adn_obj = adn(pos=DOWN*1.5, escala=1.2, color=TEAL)
        callout_obj = callout(text="Preferencia manual en fetos", color=ORANGE, font_size=60, ancho_max=7.0, pos=RIGHT*3+UP*1)

        self.play(FadeIn(prota), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(adn_obj), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(callout_obj), run_time=1)
        self.wait(12)