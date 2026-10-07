from manim import *
from zenn_rig import *

class S15(Scene):
    def construct(self):
        banda = banda_titulo("Obras que apenas circularon", color=TEAL)
        prota = protagonista(DOWN * 1.4 + LEFT * 3.6, playera="verde", altura=2.5,
                             expresion="triste", pose="de_pie")
        libro = caja("LATÍN", pos=LEFT * 1.6 + UP * 0.4, width=1.5)
        barrera = red_seguridad(width=3.4, height=0.7, pos=RIGHT * 1.1 + UP * 0.5)
        dato = etiqueta("Ignoradas en Occidente", (3.7, 1.4), color=RED)
        centro = etiqueta("centros de estudio", (3.7, -1.6))

        self.play(Write(banda), FadeIn(prota), run_time=0.9)
        self.play(FadeIn(libro, shift=UP * 0.3), run_time=0.7)
        self.play(Create(barrera), run_time=0.8)
        self.play(libro.animate.shift(RIGHT * 2.5), run_time=1.0)
        self.play(Indicate(barrera, color=RED, scale_factor=1.15), run_time=0.5)
        self.play(libro.animate.shift(LEFT * 1.0), run_time=0.5)
        self.play(FadeIn(dato), FadeIn(centro), run_time=0.7)
        self.wait(0.6)