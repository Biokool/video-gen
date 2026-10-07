from manim import *
from zenn_rig import *

class S015(Scene):
    def construct(self):
        cells = estrellas(n=80, seed=7, color=INK)
        prota = protagonista(pos=ORIGIN, playera=PLAYERA_AZUL, altura=3.0,
                             expresion='decidido', pose='de_pie')
        mano = stick_idle(pos=RIGHT*2.0+UP*0.5, height=0.5, color=INK)

        self.add(cells)
        self.play(FadeIn(prota), FadeIn(mano), run_time=1.0)
        self.play(mano.animate.shift(DOWN*0.3), run_time=0.5)
        self.play(mano.animate.shift(UP*0.3), run_time=0.5)
        self.wait(0.5)