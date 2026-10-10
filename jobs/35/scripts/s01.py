from manim import *
from zenn_rig import *

class S01(Scene):
    def construct(self):
        # Tarjeta de canal
        self.play(FadeIn(tarjeta_canal("Indaga")), run_time=1)
        self.wait(1)

        # Protagonista EL PORQUÉ (naranja, señalando, expresión feliz)
        prota = protagonista(
            pos=ORIGIN,
            playera='naranja',
            altura=3.0,
            expresion='feliz',
            pose='senalando'
        )
        self.play(FadeIn(prota), run_time=1)
        self.wait(1)

        # Mantener la escena un tiempo adicional para llegar a ~13 s
        self.wait(9)