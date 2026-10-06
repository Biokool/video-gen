from manim import *
from zenn_rig import *

class S033(Scene):
    def construct(self):
        # Protagonista con playera roja, expresión pensando
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera="roja",
            altura=2.5,
            expresion="pensando",
            pose="de_pie"
        )

        # Cerebro representado por una curva (niebla mental)
        cerebro = curva(
            pos=RIGHT*2 + UP*0.5,
            ancho=2.2,
            alto=1.5,
            color=INK,
            acento=RED
        )

        # Reloj lento
        reloj = reloj_pared(
            radius=0.8,
            pos=RIGHT*2 + DOWN*1.0,
            hora_3=True
        )

        # Etiquetas explicativas
        etiqueta_niebla = etiqueta(
            "niebla mental",
            (RIGHT*2 + UP*0.5 + UP*0.8),
            color=INK,
            font_size=30
        )
        etiqueta_lento = etiqueta(
            "lento",
            (RIGHT*2 + DOWN*1.0 + UP*0.5),
            color=INK,
            font_size=30
        )

        # Animaciones
        self.play(FadeIn(prota), run_time=1.0)
        self.play(Create(cerebro), run_time=1.0)
        self.play(Create(reloj), run_time=1.0)
        self.play(FadeIn(etiqueta_niebla), FadeIn(etiqueta_lento), run_time=0.8)
        self.wait(1.0)