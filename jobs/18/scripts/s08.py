from manim import *
from zenn_rig import *

class S08(Scene):
    def construct(self):
        prota = protagonista(pos=ORIGIN, playera="azul", altura=3.0, expresion="pensando", pose="de_pie")
        self.play(FadeIn(prota), run_time=1.0)
        self.wait(0.5)

        sun = sol(color=YELLOW, radius=0.6, pos=prota.get_top()+UP*0.2)
        self.play(FadeIn(sun), run_time=0.8)
        self.wait(0.3)

        on_label = callout(text="ON", color=ORANGE, font_size=40)
        on_label.next_to(prota.get_left(), LEFT, buff=0.5).align_to(prota.get_top(), UP)
        arr = arrow(start=on_label.get_right(), end=prota.get_left()+RIGHT*0.1, color=INK, width=8)
        self.play(FadeIn(on_label), GrowArrow(arr), run_time=1.0)
        self.wait(0.5)