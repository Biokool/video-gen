from manim import *
from zenn_rig import *

class S01(Scene):
    def construct(self):
        # Título superior (único en la escena)
        titulo = banda_titulo(
            "El mito del casco vikingo",
            color=ORANGE,
        )

        # Protagonista (versión 1: playera naranja) posicionado bajo la banda
        prota = version_prota(
            1,
            pos=DOWN * 1.2 + LEFT * 3.5,
            altura=2.6,
        )

        # Prop principal: casco vikingo centrado a la derecha
        casco = casco_vikingo(
            pos=RIGHT * 2 + UP * 0.5,
            escala=1.0,
        )

        # Monigote secundario como contraste
        stick = stick_idle(
            pos=RIGHT * 2 + DOWN * 0.5,
            height=2.2,
            color=INK,
        )

        # Texto secundario (etiqueta) al lado opuesto del protagonista
        dato = etiqueta(
            "¿Casco con cuernos?",
            pos=RIGHT * 3.4 + UP * 1,
            color=ORANGE,
            font_size=40,
            ancho_max=5.5,
        )

        # Animaciones
        self.play(FadeIn(titulo))
        self.wait(0.5)

        self.play(FadeIn(prota))
        self.play(FadeIn(casco))
        self.play(FadeIn(stick))
        self.wait(0.5)

        self.play(FadeIn(dato))
        self.wait(2)