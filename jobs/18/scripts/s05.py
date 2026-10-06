from manim import *
from zenn_rig import *

class S05(Scene):
    def construct(self):
        self.add(fondo(INK))
        prota = protagonista(pos=LEFT*2 + DOWN*0.5, playera="azul", altura=2.5,
                             expresion="decidido", pose="senalando")
        luz = Rectangle(width=4, height=0.2, color=BLUE, fill_opacity=0.8)\
                .shift(RIGHT*2 + UP*0.5)
        aviso = callout("Luz azul ≈460 nm", color=ORANGE, font_size=96)\
                .shift(UP*2)

        self.play(FadeIn(prota), run_time=1)
        self.play(Create(luz), run_time=1)
        self.play(FadeIn(aviso), run_time=1)
        self.wait(5)