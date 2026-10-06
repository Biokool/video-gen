from manim import *
from zenn_rig import *

class S05(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3.5 + DOWN*0.5, playera=PLAYERA_NARANJA, altura=2.6, expresion='pensando', pose='de_pie')
        silueta = stick_idle(pos=RIGHT*3.5 + DOWN*0.5, height=2.2, color=INK)
        signo = callout(text="?", color=ORANGE)
        self.play(FadeIn(prota), FadeIn(silueta), FadeIn(signo), run_time=1.5)
        self.wait(2.5)