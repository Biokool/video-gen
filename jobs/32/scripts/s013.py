from manim import *
from zenn_rig import *

class S013(Scene):
    def construct(self):
        prota = protagonista(
            pos=DOWN*1.2+LEFT*3.5,
            playera=PLAYERA_AZUL,
            altura=2.6,
            expresion="pensando",
            pose="de_pie"
        )
        kidney = curva(
            pos=RIGHT*2,
            ancho=2.2,
            alto=1.2,
            color=TEAL,
            acento=RED
        )
        arrow_mob = arrow(
            start=kidney.get_right(),
            end=kidney.get_right()+RIGHT*1.5,
            color=INK,
            width=8
        )
        droplet = etiqueta(
            "💧",
            pos=RIGHT*4.5,
            color=INK,
            font_size=40,
            ancho_max=5.5
        )

        self.play(FadeIn(prota), run_time=1)
        self.wait(0.5)
        self.play(Create(kidney), run_time=1)
        self.wait(0.3)
        self.play(GrowArrow(arrow_mob), run_time=0.8)
        self.wait(0.2)
        self.play(FadeIn(droplet), run_time=0.8)
        self.wait(1)