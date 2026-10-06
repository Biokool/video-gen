from manim import *
from zenn_rig import *

class S021(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*2, playera="verde", altura=2.6, expresion='normal', pose='de_pie')
        self.play(FadeIn(prota), run_time=0.8)
        self.wait(0.2)
        cambiar_cara(prota, "pensando")
        self.wait(0.2)

        plasma_bar = Rectangle(width=0.8, height=2.0, fill_color=YELLOW, fill_opacity=0.8, stroke_color=INK)
        plasma_bar.move_to(RIGHT*2)
        self.play(Create(plasma_bar), run_time=0.8)
        self.wait(0.2)

        arrow_down = arrow(start=plasma_bar.get_top(), end=plasma_bar.get_bottom(), color=INK, width=8)
        self.play(FadeIn(arrow_down), run_time=0.5)
        self.wait(0.2)

        self.play(plasma_bar.animate.stretch(0.3, dim=1, about_point=plasma_bar.get_bottom()), run_time=1.5)
        self.wait(0.5)