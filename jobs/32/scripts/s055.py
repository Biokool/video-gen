from manim import *
from zenn_rig import *

class S055(Scene):
    def construct(self):
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera="teal",
            altura=2.4,
            expresion="pensando",
            pose="de_pie"
        )
        tarjeta = tarjeta_canal()
        self.play(FadeIn(prota), FadeIn(tarjeta), run_time=1.5)
        self.wait(0.5)