from manim import *
from zenn_rig import *

class S24(Scene):
    def construct(self):
        self.add(fondo(INK))
        stars = estrellas(15)
        self.play(FadeIn(stars), run_time=1.0)
        
        fig = stick_idle(pos=LEFT * 3, height=2.2, color=WHITE)
        self.play(FadeIn(fig), run_time=1.0)
        
        puzzle = VGroup()
        for i in range(3):
            for j in range(3):
                piez = Square(side_length=0.8, color=YELLOW, fill_opacity=0.8)
                piez.move_to([LEFT * 1 + i * 0.9, UP * 1 + j * 0.9, 0])
                puzzle.add(piez)
        self.play(FadeIn(puzzle), run_time=1.5)
        
        missing = Square(side_length=0.8, color=RED, fill_opacity=0.0, stroke_width=3)
        missing.move_to([ORIGIN, 0])
        self.play(Create(missing), run_time=1.0)
        
        thought = stick_think(fig, "¿Dónde está?")
        self.play(FadeIn(thought), run_time=1.0)
        
        expresion(fig, "preocupado")
        
        callout1 = callout("50 años...", color=ORANGE, font_size=72)
        callout1.to_edge(UP)
        self.play(Write(callout1), run_time=1.5)
        
        self.wait(1.0)
        
        callout2 = callout("Invisible", color=ORANGE, font_size=72)
        callout2.next_to(callout1, DOWN, buff=0.5)
        self.play(Write(callout2), run_time=1.5)
        
        fig2 = stick_idle(pos=RIGHT * 3, height=2.2, color=WHITE)
        self.play(FadeIn(fig2), run_time=0.5)
        stick_point(fig2, missing)
        
        self.wait(1.0)
        
        self.play(FadeOut(callout1), FadeOut(callout2), run_time=1.0)
        
        self.play(FadeOut(self.mobjects), run_time=1.0)