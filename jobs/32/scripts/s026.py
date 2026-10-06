from manim import *
from zenn_rig import *

class S026(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT*2 + DOWN*1.2,
            playera="verde",
            altura=2.4,
            expresion="pensando",
            pose="de_pie"
        )
        motor = caja("Motor 1/2 aceite", pos=RIGHT*2 + DOWN*1.2, width=1.5)
        flecha = arrow(start=motor.get_right(), end=prota.get_left(), color=INK, width=8)
        vel = etiqueta("Alta velocidad", pos=UP*2, color=INK, font_size=40, ancho_max=5.5)

        self.play(FadeIn(prota), FadeIn(motor), run_time=1)
        self.play(Create(flecha), run_time=1)
        self.play(Write(vel), run_time=1)
        self.wait(2)