from manim import *
from zenn_rig import *

class S08(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*0.5, playera=PLAYERA_AZUL, altura=2.6, expresion='pensando', pose='de_pie')
        self.play(FadeIn(prota), run_time=1)
        self.wait(0.5)

        hip = caja("Hipotálamo", pos=LEFT*3 + UP*2, width=1.5)
        self.play(FadeIn(hip), run_time=1)
        self.wait(0.2)
        self.play(Indicate(hip, scale_factor=1.25), run_time=0.5)

        cer = caja("Cerebro", pos=RIGHT*3 + UP*2, width=1.5)
        self.play(FadeIn(cer), run_time=1)
        self.wait(0.2)

        flecha = arrow(hip.get_right(), cer.get_left(), color=INK, width=8)
        self.play(Create(flecha), run_time=1)
        self.wait(1)