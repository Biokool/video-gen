from manim import *
from zenn_rig import *

class S45(Scene):
    def construct(self):
        self.add(fondo(INK))

        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera="verde", altura=2.6, expresion="sorpresa", pose="de_pie")
        self.play(FadeIn(prota), run_time=0.8)

        piedra = Circle(radius=0.2, color=WHITE).move_to(DOWN*1.8+LEFT*2.0)
        self.play(FadeIn(piedra), run_time=0.4)

        texto = "Más lejos y más rápido"
        call = callout(texto, color=ORANGE, pos=RIGHT*3.4+UP*1)
        self.play(FadeIn(call), run_time=0.5)

        arrow_obj = arrow(start=LEFT*4+UP*2, end=LEFT*2+UP*2, color=YELLOW, width=8)
        self.play(FadeIn(arrow_obj), run_time=0.2)
        self.play(arrow_obj.animate.shift(RIGHT*8), run_time=1.5)

        self.wait(0.5)