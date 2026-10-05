from manim import *
from zenn_rig import *

class S12(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*4.2 + DOWN*0.5, playera="azul", altura=3.0,
                             expresion="pensando", pose="senalando")
        ojo = ojo_grande(pos=RIGHT*4.2 + UP*0.8, escala=1.0, iris=TEAL)
        co = callout("¿Se aleja un poco?", color=ORANGE, font_size=72)

        self.play(FadeIn(prota), FadeIn(ojo), run_time=0.8)
        self.play(Write(co), run_time=1.0)
        fl = arrow(LEFT*1.0 + UP*0.8, RIGHT*3.0 + UP*0.8, color=RED, width=6)
        self.play(Create(fl), run_time=0.8)
        self.wait(1.4)