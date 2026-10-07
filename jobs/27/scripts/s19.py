from manim import *
from zenn_rig import *

class S19(Scene):
    def construct(self):
        self.add(fondo_papel())
        banda = banda_titulo("400 copias, casi 0 ventas", color=RED)
        prota = protagonista(pos=DOWN*1.2+LEFT*3.8, playera="roja",
                             altura=2.6, expresion="sorpresa", pose="senalando")
        libros = caja("libros", pos=RIGHT*2.8+DOWN*1.7, width=1.8)
        cero = etiqueta("0 ventas", (2.8, -0.5), color=RED)
        dato = etiqueta("Solo 400 copias", (3.6, 1.2), color=ORANGE)
        self.play(FadeIn(banda), FadeIn(prota), run_time=1.0)
        self.play(FadeIn(libros, shift=UP*0.3), run_time=0.8)
        self.play(Write(cero), run_time=0.7)
        self.play(FadeIn(dato, scale=0.9), run_time=0.7)
        self.play(prota.animate.shift(RIGHT*0.3), run_time=0.6)
        cambiar_cara(prota, "mente_explotada")
        self.wait(1.2)
        self.play(Indicate(dato, color=YELLOW), run_time=1.0)
        self.wait(2.0)