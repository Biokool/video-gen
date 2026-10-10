from manim import *
from zenn_rig import *

class S98(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2+LEFT*2, playera=PLAYERA_NARANJA, altura=2.5, expresion='pensando', pose='de_pie')
        dna = adn(pos=RIGHT*2, escala=1.2, color=TEAL)
        q = callout("¿Qué otras verdades son maleables?", color=ORANGE, font_size=40, pos=RIGHT*3.4+UP*1)

        self.play(FadeIn(prota), run_time=1.5)
        self.play(FadeIn(dna), run_time=1.5)
        self.play(FadeIn(q), run_time=1.5)
        self.wait(4.0)
        self.play(dna.animate.scale(1.25).set_color(RED), run_time=1.0)
        self.wait(1.0)