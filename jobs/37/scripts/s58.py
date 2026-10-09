from manim import *
from zenn_rig import *

class S58(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*4, playera=PLAYERA_NARANJA, altura=2.6, expresion='feliz', pose='de_pie')
        stick = stick_idle(pos=LEFT*1, height=2.2, color=INK)
        opera = casa(pos=RIGHT*2, size=1.6)

        self.play(FadeIn(prota), FadeIn(stick), FadeIn(opera), run_time=1.0)
        self.wait(0.5)
        # Assuming stick_point returns a mobject that needs to be created
        self.play(Create(stick_point(stick, opera.get_center())), run_time=1.0)
        self.wait(1.0)