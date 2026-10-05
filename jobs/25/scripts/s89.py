from manim import *
from zenn_rig import *

class S89(Scene):
    def construct(self):
        # Protagonista principal: EL PORQUÉ
        prota = protagonista(
            pos=LEFT * 2.5 + DOWN * 0.5,
            playera="naranja",
            expresion="feliz",
            pose="senalando",
        )

        # Gran ojo curioso como compañero visual
        ojo = ojo_grande(pos=RIGHT * 2.5 + UP * 0.5, escala=0.9, iris=TEAL)

        self.play(FadeIn(prota), FadeIn(ojo))
        self.wait(1)

        # Llamado a suscribirse
        call = callout("¡Suscríbete!", color=ORANGE, font_size=72)
        self.play(FadeIn(call, shift=UP))
        self.wait(3)

        # Despedida
        self.play(FadeOut(call, shift=UP), FadeOut(prota), FadeOut(ojo))
        self.wait(1)