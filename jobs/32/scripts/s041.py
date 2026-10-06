from manim import *
from zenn_rig import *

class S041(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3.5 + DOWN*1.2, playera=PLAYERA_AMARILLA, altura=2.5, expresion='pensando', pose='de_pie')
        brain = curva(pos=RIGHT*3.5, ancho=5.2, alto=2.8, color=INK, acento=RED)
        shield = red_seguridad(width=4.5, height=0.7, pos=DOWN*1.5)
        txt = callout("Mientras tu cerebro lucha, tus células están librando su propia batalla.")
        txt.shift(UP*2)

        self.play(FadeIn(prota), run_time=1.0)
        self.play(Create(brain), run_time=1.0)
        self.play(FadeIn(shield), run_time=1.0)
        self.play(Write(txt), run_time=1.0)
        self.wait(1.0)