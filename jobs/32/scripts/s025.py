from manim import *
from zenn_rig import *

class S025(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera="verde", altura=2.6, expresion='sorpresa', pose='de_pie')
        callout_txt = callout(text="1%", color=ORANGE, pos=RIGHT*3.4+UP*1)
        latido = etiqueta("+3-5 lpm", pos=ORIGIN, color=INK, font_size=40)
        heart = Circle(radius=0.3, color=RED, fill_opacity=0.6)
        heart.move_to(prota.get_center() + RIGHT*1.0 + UP*0.2)

        self.play(FadeIn(prota), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(callout_txt), run_time=0.8)
        self.wait(0.4)
        self.play(FadeIn(heart), run_time=0.6)
        self.wait(0.3)
        self.play(FadeIn(latido), run_time=0.6)
        self.wait(0.5)
        self.play(
            heart.animate.scale(1.3),
            latido.animate.scale(1.1),
            run_time=0.3
        )
        self.play(
            heart.animate.scale(1/1.3),
            latido.animate.scale(1/1.1),
            run_time=0.3
        )
        self.wait(2)
        self.play(
            heart.animate.scale(1.2),
            run_time=0.2
        )
        self.play(
            heart.animate.scale(1/1.2),
            run_time=0.2
        )
        self.wait(8)