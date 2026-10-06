from manim import *
from zenn_rig import *

class S037(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera="roja", altura=2.6, expresion="pensando", pose="de_pie")
        puzzle = etiqueta("Rompecabezas", pos=RIGHT*3.5+UP*0.5, color=INK)
        name = etiqueta("Nombre", pos=RIGHT*3.5+DOWN*0.5, color=WHITE)

        self.play(FadeIn(prota), run_time=1)
        self.play(FadeIn(puzzle), run_time=1)
        self.play(FadeIn(name), run_time=1)
        self.wait(2)
        self.play(prota.animate.shift(UP*0.2), run_time=0.5)
        self.wait(1.5)