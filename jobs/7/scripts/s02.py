from manim import *
from zenn_rig import *

class S02(Scene):
    def construct(self):
        # Protagonista (naranja, pensativo)
        prota = protagonista(pos=LEFT*4, playera=PLAYERA_NARANJA, expresion='pensando', pose='de_pie')

        # Cerebro esquemático (representado por un círculo oscuro)
        cerebro = Circle(radius=1.2, color=INK, fill_opacity=0.8).move_to(RIGHT*2)

        # Signo de interrogación flotando sobre el cerebro
        interrogacion = Text("?", color=YELLOW).scale(3).next_to(cerebro, UP, buff=0.5)

        # Animación de la escena
        self.play(FadeIn(prota), run_time=0.8)
        self.play(Create(cerebro), run_time=0.8)
        self.play(FadeIn(interrogacion, shift=UP), run_time=0.8)
        self.wait(1.6) # Duración total ~4 segundos (0.8+0.8+0.8+1.6)