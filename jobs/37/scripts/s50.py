from manim import *
from zenn_rig import *

class S50(Scene):
    def construct(self):
        # Protagonista a la izquierda, abajo
        prota = protagonista(
            pos=LEFT*3 + DOWN*1.2,
            playera="naranja",
            altura=2.6,
            expresion="feliz",
            pose="senalando"
        )
        # Año 1876 a la derecha
        year = Text("1876", font_size=48)
        year.move_to(RIGHT*3)
        # Aplicar acento rojo al año
        red_accent(year)

        # Animaciones de entrada
        self.play(FadeIn(prota, shift=UP), FadeIn(year, shift=UP), run_time=1)
        self.wait(2.5)  # total ~4 segundos
        self.play(FadeOut(prota), FadeOut(year), run_time=0.5)