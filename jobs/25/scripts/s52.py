from manim import *
from zenn_rig import *

class S52(Scene):
    def construct(self):
        p = protagonista(
            LEFT * 4 + UP * 0.2,
            playera="amarilla",
            altura=2.6,
            expresion="pensando",
            pose="senalando"
        )
        ojo = ojo_grande(RIGHT * 3.8 + UP * 1.4, escala=0.9, iris=TEAL)
        espectro = curva(
            RIGHT * 2.8 + DOWN * 0.6,
            ancho=2.8,
            alto=1.5,
            color=AZUL_MARINO,
            acento=RED
        )
        etiqueta_esp = etiqueta(
            "ESPECTRO",
            (0.0, 2.8),
            color=AZUL_MARINO,
            font_size=36
        )

        self.play(FadeIn(p, shift=LEFT * 0.4), run_time=1.0)
        self.play(FadeIn(ojo, shift=UP * 0.4), run_time=1.0)
        self.play(Create(espectro), run_time=1.8)
        self.play(FadeIn(etiqueta_esp, shift=DOWN * 0.2), run_time=0.8)
        self.wait(1.4)