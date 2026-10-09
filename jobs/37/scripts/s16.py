from manim import *
from zenn_rig import *

class S16(Scene):
    def construct(self):
        # Fondo claro (opcional)
        self.add(fondo(WHITE))

        # --------------------------------------------------------------------
        # Título superior
        # --------------------------------------------------------------------
        titulo = banda_titulo("Diferencia de 2 000 años", color=ORANGE)
        self.play(FadeIn(titulo, shift=UP))
        self.wait(1)

        # --------------------------------------------------------------------
        # Protagonista a la izquierda, expresión pensativa
        # --------------------------------------------------------------------
        prota = protagonista(
            pos=LEFT * 4 + DOWN * 1.2,
            playera=PLAYERA_NARANJA,
            altura=2.6,
            expresion="pensando",
            pose="de_pie",
        )
        self.add(prota)
        self.play(FadeIn(prota, shift=RIGHT))
        self.wait(0.5)

        # --------------------------------------------------------------------
        # Monigote clásico a la derecha (idle)
        # --------------------------------------------------------------------
        monigote = stick_idle(
            pos=RIGHT * 3 + DOWN * 1.2,
            height=2.2,
            color=INK,
        )
        self.play(FadeIn(monigote, shift=LEFT))
        self