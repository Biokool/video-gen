from manim import *
from zenn_rig import *

class S030(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT*2 + DOWN*0.5,
            playera='roja',
            altura=2.6,
            expresion='pensando',
            pose='de_pie'
        )
        cerebro = matraz(
            pos=RIGHT*2 + UP*0.5,
            escala=1.2,
            liquido=TEAL
        )
        mente = ojo_grande(
            pos=RIGHT*2 + DOWN*1.5,
            escala=1.2,
            iris=TEAL
        )

        self.play(FadeIn(prota), run_time=1.0)
        self.play(Create(cerebro), run_time=1.0)
        self.play(FadeIn(mente), run_time=1.0)
        self.wait(1.0)