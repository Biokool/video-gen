from manim import *
from zenn_rig import *

class S03(Scene):
    def construct(self):
        prota = protagonista(pos=ORIGIN, playera='naranja', expresion='sorpresa')
        self.play(FadeIn(prota, shift=UP))

        ojo = ojo_grande(pos=RIGHT * 3.5, escala=1.2)
        self.play(Create(ojo))

        boom = callout("¡BOOM!", color=RED)
        boom.to_edge(UP, buff=0.2)
        self.play(Write(boom))

        cambiar_cara(prota, 'mente_explotada')
        self.wait(0.2)

        self.add(red_accent(prota))
        self.wait(0.8)