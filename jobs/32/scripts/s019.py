from manim import *
from zenn_rig import *

class S019(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*4 + DOWN*0.5, playera="verde", altura=2.6, expresion="pensando", pose="de_pie")
        riverbed = camino(width=7.0, pos=DOWN*1.0)
        water = curva(pos=UP*0.5, ancho=5.0, alto=0.2, color=INK, acento=RED)
        msg = callout(text="Lento y espeso", color=ORANGE, font_size=96)
        msg.move_to(RIGHT*4 + UP*2)
        self.play(FadeIn(prota), Create(riverbed), Create(water), FadeIn(msg), run_time=1.5)
        self.wait(3.5)