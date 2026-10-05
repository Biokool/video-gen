from manim import *
from zenn_rig import *

class S70(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=42, seed=7, color=WHITE))

        prota = protagonista(
            pos=LEFT * 2.7 + DOWN * 0.2,
            playera=PLAYERA_NARANJA,
            altura=3.0,
            expresion="decidido",
            pose="de_pie",
        )
        self.play(FadeIn(prota, shift=UP * 0.6), run_time=0.6)
        self.wait(0.2)

        ojo = ojo_grande(pos=RIGHT * 3.3 + UP * 1.0, escala=1.2, iris=TEAL)
        self.play(Create(ojo), run_time=0.8)
        self.wait(0.2)

        simbolo = moneda_dorada(
            texto="S",
            pos=prota.get_center() + UP * 0.3,
            radio=0.45,
        )
        self.play(FadeIn(simbolo, scale=2.0), run_time=0.5)
        self.wait(0.2)

        cambiar_cara(prota, "euforico")
        self.play(prota.animate.shift(RIGHT * 0.3), run_time=0.4)
        self.wait(0.6)