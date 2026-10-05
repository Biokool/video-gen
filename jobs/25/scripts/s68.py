from manim import *
from zenn_rig import *

class S68(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT * 3.0,
            playera="amarilla",
            altura=3.0,
            expresion="pensando",
            pose="de_pie",
        )
        ojo = ojo_grande(pos=RIGHT * 3.2, escala=1.2, iris=TEAL)
        signo = callout("¿CÓMO?", color=YELLOW).shift(UP * 2.2)

        self.play(FadeIn(prota), run_time=1.0)
        self.play(FadeIn(ojo), run_time=1.0)
        self.play(GrowFromCenter(signo), run_time=0.8)
        self.wait(1.2)