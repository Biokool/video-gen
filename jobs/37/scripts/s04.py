from manim import *
from zenn_rig import *

class S04(Scene):
    def construct(self):
        # Protagonista con playera azul, señalando
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera="azul",
            altura=2.6,
            expresion="decidido",
            pose="senalando"
        )
        # Icono de película
        movie_caja = caja(etiqueta="🎬", pos=LEFT*4 + UP*1, width=1.5)
        # Icono de serie
        serie_caja = caja(etiqueta="📺", pos=LEFT*4 + DOWN*1, width=1.5)
        # Callout con el número cero
        zero_callout = callout(
            text="0",
            color=ORANGE,
            font_size=60,
            pos=RIGHT*3.4 + UP*1
        )

        # Animaciones
        self.play(FadeIn(prota), run_time=1)
        self.wait(2)
        self.play(FadeIn(movie_caja), FadeIn(serie_caja), run_time=1.5)
        self.wait(2)
        self.play(FadeIn(zero_callout), run_time=1)
        self.wait(10)  # completar duración aproximada de ~18 segundos