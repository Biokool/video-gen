from manim import *
from zenn_rig import *

class S51(Scene):
    def construct(self):
        prop = curva(pos=RIGHT*2, ancho=5.2, alto=2.8, color=INK, acento=RED)
        stick = stick_idle(pos=LEFT*2, height=2.2, color=INK)
        expresion(stick, tipo='normal')
        prota = protagonista(pos=LEFT*4 + DOWN*1.5, playera='naranja', altura=2.6, expresion='pensando', pose='de_pie')
        self.play(FadeIn(prota), run_time=0.8)
        self.play(Create(prop), run_time=0.8)
        self.play(Create(stick), run_time=0.8)
        # Point using an arrow from the stick figure to the curve
        pointer = arrow(start=stick.get_center(), end=prop.get_center(), color=INK, width=8)
        self.play(Create(pointer), run_time=0.8)
        self.wait(0.8)