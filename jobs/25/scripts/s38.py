from manim import *
from zenn_rig import *

class S38(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT * 3.5,
            playera="amarilla",
            altura=2.8,
            expresion="pensando",
            pose="de_pie",
        )
        ojo = ojo_grande(pos=RIGHT * 3.2 + UP * 0.4, escala=0.8, iris=TEAL)
        flecha = arrow(
            start=RIGHT * 1.2 + DOWN * 1.0,
            end=RIGHT * 1.2 + UP * 2.8,
            color=INK,
            width=8,
        )

        self.add(prota)
        self.play(FadeIn(prota, run_time=1.0))
        self.wait(0.5)

        self.play(FadeIn(ojo, run_time=0.8))
        self.wait(0.3)

        self.play(Create(flecha, run_time=1.2))
        cambiar_cara(prota, "sorpresa")
        self.wait(1.2)