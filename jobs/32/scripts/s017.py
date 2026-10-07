from manim import *
from zenn_rig import *

class S017(Scene):
    def construct(self):
        # Protagonista con expresión de sorpresa, camisa azul
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera="azul",
            altura=2.6,
            expresion="sorpresa",
            pose="de_pie"
        )

        # Vaso que representa sangre vacía (caja con etiqueta)
        vaso = caja("Sangre vacío", pos=RIGHT*2 + DOWN*0.5, width=1.5)

        # Signo de interrogación como callout destacado
        signo = callout("?", color=ORANGE, pos=RIGHT*4 + UP*1)

        # Animaciones secuenciales
        self.play(FadeIn(prota), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(vaso), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(signo), run_time=1.0)
        self.wait(2.0)  # completar ~6 segundos total