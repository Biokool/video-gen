from manim import *
from zenn_rig import *

class S015(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=40, seed=7, color=WHITE))

        prota = protagonista(pos=ORIGIN, playera=PLAYERA_AZUL, altura=2.8, expresion='determinado')
        gota = callout(text="Última gota", color=ORANGE)
        gota.shift(UP*1.5 + RIGHT*2)

        self.play(FadeIn(prota, shift=DOWN*0.5), run_time=1.0)
        self.play(FadeIn(gota, shift=UP*0.5), run_time=0.8)
        self.wait(2.0)