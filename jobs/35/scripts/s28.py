from manim import *
from zenn_rig import *

class S28(Scene):
    def construct(self):
        prota = protagonista(pos=ORIGIN, playera="verde", altura=3.0, expresion="sorpresa", pose="de_pie")
        brain_left = personaje(pos=LEFT*3, cuerpo=TEAL, altura=2.0, expresion_tipo="normal")
        brain_right = personaje(pos=RIGHT*3, cuerpo=TEAL, altura=2.0, expresion_tipo="normal")
        fig = stick_idle(pos=DOWN*1.5, height=2.2, color=INK)

        self.play(FadeIn(prota), FadeIn(brain_left), FadeIn(brain_right), run_time=1.5)
        self.wait(0.5)
        self.play(Create(fig), run_time=1.0)
        self.wait(0.3)
        self.play(Create(stick_point(fig, prota.get_center())))
        self.wait(0.2)
        self.play(brain_left.animate.shift(LEFT*0.2), brain_right.animate.shift(RIGHT*0.2), run_time=0.8)
        self.wait(0.2)
        self.play(brain_left.animate.shift(RIGHT*0.2), brain_right.animate.shift(LEFT*0.2), run_time=0.8)
        self.wait(0.5)