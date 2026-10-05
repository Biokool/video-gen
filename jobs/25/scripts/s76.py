from manim import *
from zenn_rig import *

class S76(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=24, seed=12))

        prota = protagonista(
            pos=LEFT * 3.6 + DOWN * 0.2,
            playera=PLAYERA_NARANJA,
            altura=2.8,
            expresion='pensando',
            pose='de_pie'
        )
        ojo = ojo_grande(pos=RIGHT * 3.2 + UP * 1.2, escala=1.0)
        self.play(FadeIn(prota), FadeIn(ojo))

        entrantes = VGroup(
            arrow(RIGHT * 7 + UP * 1.3, ojo.get_center(), color=YELLOW, width=5),
            arrow(RIGHT * 7, ojo.get_center(), color=YELLOW, width=5),
            arrow(RIGHT * 7 - UP * 1.3, ojo.get_center(), color=YELLOW, width=5),
        )
        self.play(
            LaggedStart(*[Create(r) for r in entrantes], lag_ratio=0.25, run_time=1.3)
        )

        expandidos = VGroup(
            arrow(ojo.get_center(), RIGHT * 7 + UP * 2.3, color=ORANGE, width=5),
            arrow(ojo.get_center(), RIGHT * 7, color=ORANGE, width=5),
            arrow(ojo.get_center(), RIGHT * 7 - UP * 2.3, color=ORANGE, width=5),
        )
        self.play(
            LaggedStart(*[Create(r) for r in expandidos], lag_ratio=0.25, run_time=1.3)
        )

        cambiar_cara(prota, 'sorpresa')
        self.wait(0.8)