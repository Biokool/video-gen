from manim import *
from zenn_rig import *

class S23(Scene):
    def construct(self):
        # Stick figure appears on the left
        stick = stick_idle(LEFT * 3, height=2.2, color=INK)
        self.play(FadeIn(stick))
        self.wait(0.5)

        # Walk toward the center of the screen
        self.play(stick_walk(stick, RIGHT * 2, run_time=2.0))
        self.wait(0.5)

        # Point to the empty space on the right
        target = RIGHT * 3
        self.play(stick_point(stick, target))
        self.wait(0.5)

        # Invisible “dark matter” region (transparent circle)
        dark_region = Circle(radius=1.5, color=WHITE).move_to(RIGHT * 4)
        dark_region.set_fill(opacity=0.0)
        self.play(FadeIn(dark_region))
        self.play(red_accent(dark_region))
        self.wait(0.5)

        # Brief callout indicating invisibility
        note = callout("Invisible", color=ORANGE, font_size=96)
        note.next_to(dark_region, UP)
        self.play(FadeIn(note, scale=0.5))
        self.wait(1)

        # Fade everything out
        self.play(FadeOut(stick), FadeOut(dark_region), FadeOut(note))
        self.wait(0.5)