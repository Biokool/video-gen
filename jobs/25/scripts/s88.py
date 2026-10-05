from manim import *
from zenn_rig import *

class S88(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT * 3.2 + DOWN * 0.5,
            playera=PLAYERA_AMARILLA,
            altura=3.0,
            expresion="decidido",
            pose="senalando",
        )
        self.play(FadeIn(prota, run_time=1.0))

        ojo = ojo_grande(pos=RIGHT * 2.8 + UP * 1.8, escala=0.8)
        brujula = moneda_dorada(texto="N", pos=RIGHT * 0.5 + UP * 1.4, radio=0.5)
        mapa = camino(pos=RIGHT * 1.5 + DOWN * 1.2, width=5.0)

        self.play(Create(mapa, run_time=1.5))
        self.play(
            FadeIn(ojo, run_time=1.0),
            FadeIn(brujula, run_time=1.0),
        )
        self.wait(1.5)