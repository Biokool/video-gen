from manim import *
from zenn_rig import *

class S039(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3.5 + DOWN*1.0, playera="roja", altura=2.5, expresion="confuso", pose="de_pie")
        nube = planeta(pos=RIGHT*3.0 + UP*1.0, radio=0.8, color=WHITE)
        tortuga = personaje(pos=RIGHT*3.0 + DOWN*1.0, cuerpo=GREEN, altura=1.5, expresion_tipo="normal")
        self.play(FadeIn(prota), run_time=1.0)
        self.play(FadeIn(nube), run_time=1.0)
        self.play(FadeIn(tortuga), run_time=1.0)
        self.wait(1.0)