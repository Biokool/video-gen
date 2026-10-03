from manim import *
from zenn_rig import *

class S17(Scene):
    def construct(self):
        detector = caja("XENON", pos=DOWN * 1.6, width=2.4)
        rock = red_seguridad(width=7.5, height=1.2, pos=UP * 1.9)
        researcher = stick_idle(pos=LEFT * 4.0 + DOWN * 0.2, height=2.0, color=INK)
        researcher.add(expresion(researcher, "preocupado"))

        self.play(
            FadeIn(rock),
            FadeIn(detector),
            FadeIn(researcher),
            run_time=1.5
        )

        self.play(
            stick_walk(researcher, RIGHT * 2.0 + DOWN * 0.2, run_time=2.5, steps=7)
        )

        self.play(stick_point(researcher, detector), run_time=1.0)

        accent = red_accent(detector, scale=1.35)
        if isinstance(accent, Animation):
            self.play(accent, run_time=0.8)
        else:
            self.play(FadeIn(accent), run_time=0.8)

        label1 = callout("Miles de metros", color=ORANGE, font_size=64)
        label1.shift(UP * 3.3)
        self.play(FadeIn(label1), run_time=0.8)
        self.wait(1.0)

        label2 = callout("Destellos", color=RED, font_size=72)
        label2.shift(UP * 0.7 + RIGHT * 3.0)
        self.play(FadeIn(label2), run_time=0.8)
        self.wait(1.0)

        self.play(stick_think(researcher, "¿Impactos?"), run_time=1.2)
        self.wait(1.4)