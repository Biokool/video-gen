from manim import *
from zenn_rig import *

class S24(Scene):
    def construct(self):
        # Fondo nocturno
        self.add(fondo(INK))

        # Estrellas y luna
        self.play(FadeIn(estrellas(n=30, seed=5, color=WHITE)))
        self.play(FadeIn(luna(pos=UP * 2.5, radio=1.0, color=YELLOW, bg=INK)))

        # Stick figure a la izquierda
        stick = stick_idle(pos=LEFT * 3, height=2.2, color=INK)
        self.play(FadeIn(stick))

        # Protagonista a la derecha (versión 1: playera naranja)
        prota = version_prota(1, pos=RIGHT * 2)
        self.play(FadeIn(prota))

        # El stick señala al protagonista
        # stick_point expects a *position*, not a Mobject
        self.play(stick_point(stick, prota.get_center()))

        # El stick piensa algo
        self.play(stick_think(stick, "¿Qué pasa?"))

        # Cambiamos la expresión del protagonista a sorpresa
        self.play(cambiar_cara(prota, "sorpresa"))

        # Tarjeta de título
        titulo = title_card("Noche misteriosa", color=YELLOW)
        self.play(FadeIn(titulo))
        self.wait(2)
        self.play(FadeOut(titulo))
        self.wait(1)