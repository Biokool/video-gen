from manim import *
from zenn_rig import *

class S17(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera="azul", altura=2.6, expresion="confundido", pose="de_pie")
        romano = stick_idle(pos=LEFT*2, height=2.2, color=RED)
        soldado = stick_idle(pos=RIGHT*2, height=2.2, color=YELLOW)

        self.play(FadeIn(prota, shift=UP), run_time=0.4)
        self.wait(0.3)
        self.play(FadeIn(romano, shift=UP), run_time=0.4)
        self.wait(0.2)
        self.play(FadeIn(soldado, shift=UP), run_time=0.4)
        self.wait(0.2)
        self.wait(2.0)
        self.play(FadeOut(prota, shift=DOWN), FadeOut(romano, shift=DOWN), FadeOut(soldado, shift=DOWN), run_time=0.4)
        self.wait(0.3)