from manim import *
from zenn_rig import *

class S017(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT*3.5 + DOWN*0.5,
            playera=PLAYERA_AZUL,
            altura=2.5,
            expresion="pregunta",
            pose="senalando"
        )
        vaso = matraz(
            pos=RIGHT*2.0 + UP*0.5,
            escala=1.0,
            liquido=INK
        )
        signo = callout("?", color=ORANGE, font_size=96)
        signo.shift(RIGHT*2.0 + UP*2.0)

        self.play(FadeIn(prota), run_time=1.0)
        self.play(FadeIn(vaso), run_time=1.0)
        self.play(FadeIn(signo), run_time=1.0)
        self.wait(2.0)