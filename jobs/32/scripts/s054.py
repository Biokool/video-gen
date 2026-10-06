from manim import *
from zenn_rig import *

class S054(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3 + DOWN*0.5, playera="rosa", altura=2.6, expresion="feliz", pose="de_pie")
        earth = planeta(pos=RIGHT*3 + UP*1, radio=0.95, color=TEAL)
        notes = VGroup(
            Text("♪", font_size=40),
            Text("♪", font_size=40),
            Text("♪", font_size=40)
        ).arrange(RIGHT, buff=0.5)
        notes.next_to(prota, UP, buff=0.2)
        callout_txt = callout(text="Orquesta de adaptaciones", color=ORANGE, font_size=96)
        callout_txt.to_edge(UP)

        self.play(FadeIn(prota), run_time=1.5)
        self.play(FadeIn(earth), run_time=1.0)
        self.play(Write(notes), run_time=1.5)
        self.play(FadeIn(callout_txt), run_time=1.0)
        self.wait(2.5)