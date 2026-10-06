from manim import *
from zenn_rig import *

class S06(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera="naranja", altura=2.6, expresion="sorprendido", pose="de_pie")
        brain = Circle(radius=0.8, color=INK, fill_opacity=0.2)
        brain.move_to(RIGHT*2+UP*0.5)
        red_brain = red_accent(brain, scale=1.25)
        txt = callout("1%", color=ORANGE, font_size=96)
        txt.next_to(brain, UP)

        self.play(FadeIn(prota), run_time=1.0)
        self.play(Create(brain), run_time=1.0)
        self.play(FadeIn(red_brain), run_time=0.5)
        self.play(FadeIn(txt), run_time=0.8)
        self.wait(3.5)