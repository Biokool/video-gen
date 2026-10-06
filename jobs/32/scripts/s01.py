from manim import *
from zenn_rig import *

class S01(Scene):
    def construct(self):
        prota = protagonista(pos=ORIGIN, playera=PLAYERA_NARANJA, altura=3.0, expresion='feliz', pose='de_pie')
        tarjeta = tarjeta_canal(texto='EL PORQUÉ', subtitulo='curiosidad científica')
        self.play(FadeIn(prota), FadeIn(tarjeta), run_time=2)
        self.wait(4)
        self.play(FadeOut(prota), FadeOut(tarjeta), run_time=2)
        self.wait(1)