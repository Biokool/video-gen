from manim import *
from zenn_rig import *

class S02(Scene):
    def construct(self):
        # agujero negro minimalista
        black_hole = Circle(radius=1, color=INK, fill_opacity=0.9).shift(3 * RIGHT)
        self.play(FadeIn(black_hole, shift=UP))

        # monigote curioso con signo de interrogación
        stick = stick_idle(pos=3 * LEFT, height=2.2, color=INK)
        self.play(FadeIn(stick, shift=UP))

        question = Text("?", font_size=96, color=YELLOW).next_to(stick, UP)
        self.play(FadeIn(question, shift=UP))

        self.wait(0.5)

        # camina hacia el agujero negro
        self.play(stick_walk(stick, black_hole.get_center(), run_time=3.0))

        # al llegar, todo desaparece
        self.play(FadeOut(stick), FadeOut(question), FadeOut(black_hole))
        self.wait(0.5)