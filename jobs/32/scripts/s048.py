from manim import *
from zenn_rig import *

class S048(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT*2 + DOWN*0.5,
            playera="amarilla",
            altura=2.6,
            expresion="pensando",
            pose="de_pie"
        )
        domino = caja(etiqueta="", pos=ORIGIN, width=0.8)
        peligro = fuego(pos=RIGHT*2 + DOWN*0.5, escala=1.0)

        self.play(FadeIn(prota), run_time=1)
        self.wait(0.3)
        self.play(Create(domino), run_time=0.8)
        self.play(Rotate(domino, angle=-PI/4, about_point=domino.get_center()), run_time=0.6)
        self.wait(0.2)
        self.play(FadeIn(peligro), run_time=0.8)
        self.wait(1.2)