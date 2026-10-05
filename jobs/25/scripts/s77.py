from manim import *
from zenn_rig import *

class S77(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT * 4.5,
            playera="naranja",
            altura=3.0,
            expresion="sorpresa",
            pose="senalando"
        )
        ojo = ojo_grande(pos=RIGHT * 3.0, escala=1.2, iris=TEAL)
        dato1 = etiqueta("INFRARROJO", (2.8, 1.6), color=RED, font_size=36, ancho_max=4)
        dato2 = etiqueta("ULTRAVIOLETA", (2.8, -1.2), color=ORANGE, font_size=36, ancho_max=4)

        self.play(FadeIn(prota, shift=LEFT), run_time=0.6)
        self.play(Create(ojo), run_time=0.8)
        self.play(FadeIn(dato1, shift=UP), FadeIn(dato2, shift=DOWN), run_time=0.8)
        cambiar_cara(prota, "euforico")
        self.wait(0.9)