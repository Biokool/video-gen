from manim import *
from zenn_rig import *

class S13(Scene):
    def construct(self):
        # Protagonista con playera azul, expresión neutra y señalando
        prota = protagonista(
            pos=LEFT * 3.5,
            playera="azul",
            altura=3.0,
            expresion="pensando",
            pose="señalando"
        )

        # Ojo grande: la percepción visual
        ojo = ojo_grande(
            pos=RIGHT * 2.5 + UP * 1.2,
            escala=1.2,
            iris=TEAL
        )

        # Hormiga pequeña y sin detalles
        hormiga = stick_idle(
            pos=RIGHT * 1.2 + DOWN * 0.9,
            height=0.35,
            color=INK
        )

        # Entrada de los elementos
        self.play(FadeIn(prota, shift=LEFT * 0.5), run_time=0.7)
        self.play(FadeIn(ojo, shift=DOWN * 0.3), run_time=0.6)
        self.play(FadeIn(hormiga, shift=UP * 0.2), run_time=0.5)
        self.wait(1.2)