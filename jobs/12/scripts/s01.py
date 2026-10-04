from manim import *
from zenn_rig import *

class S01(Scene):
    def construct(self):
        # Fondo del canal a PANTALLA COMPLETA (no moverlo: es el fondo)
        self.add(fondo(AZUL_MARINO))

        # Tarjeta "EL PORQUÉ" a la izquierda (texto seguro: nunca se corta).
        # OJO: al estar descentrado (x=-3.5), el ancho máximo se reduce para
        # que quepa en la mitad izquierda; el auto-ajuste solo garantiza
        # el encuadre si el texto queda centrado en x=0.
        titulo = titulo_seguro("EL PORQUÉ", color=WHITE, font_size=110,
                               ancho_max=5.6)
        titulo.move_to(LEFT * 3.5 + UP * 0.7)
        subt = etiqueta("curiosidad científica", (-3.5, -0.5),
                        color=MOSTAZA, font_size=44)
        tarjeta = VGroup(titulo, subt)

        # Monigote feliz a la derecha
        stick_figure = stick_idle(pos=RIGHT * 3.8 + DOWN * 0.6,
                                 height=2.6, color=WHITE)
        cara = expresion(stick_figure, tipo="feliz")

        self.play(
            FadeIn(tarjeta, shift=RIGHT),
            FadeIn(stick_figure, shift=LEFT),
            FadeIn(cara),
            run_time=1.2,
        )
        self.wait(6)
        self.play(
            FadeOut(tarjeta),
            FadeOut(stick_figure),
            FadeOut(cara),
            run_time=1.0,
        )
