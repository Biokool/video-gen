from manim import *
from zenn_rig import *

class S22(Scene):
    def construct(self):
        # Banda superior
        banda = banda_titulo("Cuernos y el Norte", color=ORANGE)
        self.play(FadeIn(banda, shift=DOWN * 0.5))

        # Protagonista
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.5,
            playera="naranja",
            altura=2.6,
            expresion="feliz",
            pose="senalando"
        )
        self.play(FadeIn(prota, shift=UP * 0.5))
        self.wait(1)

        # Texto de apoyo
        texto = etiqueta("¿Por qué usan casco?", pos=RIGHT * 2 + UP * 1.2, font_size=40)
        self.play(Write(texto))
        self.wait(1)

        # Vikingo
        vikingo = casco_vikingo(pos=RIGHT * 2 + DOWN * 0.5, escala=1.2)
        self.play(FadeIn(vikingo))
        self.wait(1)

        # Explicación
        explicacion = etiqueta("Protección y estatus", pos=RIGHT * 2 + DOWN * 1.8, font_size=36)
        self.play(Write(explicacion))
        self.wait(2)

        # Cambio de expresión
        cambiar_cara(prota, "sorpresa")
        self.wait(1)

        cambiar_cara(prota, "feliz")
        self.wait(1)

        # Cierre
        self.play(FadeOut(explicacion), FadeOut(vikingo))
        self.wait(0.5)