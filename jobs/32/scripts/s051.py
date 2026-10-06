from manim import *
from zenn_rig import *

class S051(Scene):
    def construct(self):
        prota = protagonista(
            pos=DOWN*1.2+LEFT*3.5,
            playera="rosa",
            altura=2.4,
            expresion="pensando",
            pose="de_pie"
        )
        cuerpo = stick_idle(
            pos=DOWN*1.2+RIGHT*3.5,
            height=2.2,
            color=INK
        )
        gota = Dot(radius=0.15, color=BLUE).move_to(cuerpo.get_center()+UP*0.3)

        self.play(FadeIn(prota), FadeIn(cuerpo), run_time=1.0)
        self.play(FadeIn(gota), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(gota), run_time=0.5)
        self.wait(2.0)