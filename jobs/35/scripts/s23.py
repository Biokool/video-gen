from manim import *
from zenn_rig import *

class S23(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*2.0, playera="verde", altura=3.0, expresion='pensando', pose='de_pie')
        brain = curva(pos=UP*3.25, ancho=4.0, alto=1.5, color=INK, acento=RED)
        arrow_left = arrow(start=brain.get_left(), end=LEFT*5, color=INK, width=8)
        arrow_right = arrow(start=brain.get_right(), end=RIGHT*5, color=INK, width=8)

        self.add(prota, brain)
        self.play(Create(arrow_left, run_time=2), Create(arrow_right, run_time=2))
        self.wait(4)