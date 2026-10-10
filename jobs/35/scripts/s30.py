from manim import *
from zenn_rig import *

class S30(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3.5+DOWN*1.2, playera="verde", altura=2.6, expresion='feliz', pose='de_pie')
        stick_laugh = stick_idle(pos=RIGHT*3+UP*2, height=2.2, color=TEAL)
        stick_emocion = stick_idle(pos=RIGHT*3+0, height=2.2, color=TEAL)
        stick_walk_fig = stick_idle(pos=RIGHT*3+DOWN*2, height=2.2, color=TEAL)

        self.play(FadeIn(prota), FadeIn(stick_laugh), FadeIn(stick_emocion), FadeIn(stick_walk_fig), run_time=1.5)
        self.wait(0.5)

        self.play(FadeIn(stick_point(stick_laugh, prota.get_center()+UP*0.5)), run_time=1.0)
        self.play(FadeIn(stick_point(stick_emocion, prota.get_center())), run_time=1.0)
        self.play(FadeIn(expresion(stick_emocion, tipo='normal')), run_time=0.8)
        self.play(stick_walk(stick_walk_fig, target=LEFT*4, run_time=2.0, steps=6), run_time=2.0)
        self.wait(2.0)