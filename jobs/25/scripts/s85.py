from manim import *
from zenn_rig import *

class S85(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT * 2.4 + DOWN * 0.4,
            playera="rosa",
            altura=3.0,
            expresion="decidido",
            pose="de_pie"
        )

        ojo = ojo_grande(
            pos=RIGHT * 2.0 + UP * 0.2,
            escala=0.8,
            iris=TEAL
        )

        self.play(FadeIn(prota), run_time=0.7)
        self.wait(0.3)

        self.play(FadeIn(ojo, scale=0.6), run_time=0.8)
        self.wait(0.2)

        visor = red_accent(ojo, scale=1.3)
        self.play(Create(visor), run_time=1.0)
        self.play(visor.animate.scale(1.12), run_time=0.4)
        self.play(visor.animate.scale(1.0), run_time=0.4)

        etiqueta_visor = callout("capas ocultas", color=ORANGE, font_size=44)
        etiqueta_visor.to_edge(UP, buff=0.4)
        self.play(FadeIn(etiqueta_visor, shift=DOWN * 0.2), run_time=0.6)
        self.wait(0.6)