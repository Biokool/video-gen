from manim import *
from zenn_rig import *

class S04(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=42, seed=7, color=WHITE))

        # Se corrige el nombre de la constante de color de AZUL a AZUL_MARINO
        protagonista_obj = protagonista(pos=(-3, 0, 0), playera=AZUL_MARINO, expresion='pensando', pose='senalando')
        ojo_distorsionado = ojo_grande(pos=(3, 0, 0), escala=1.5, iris=RED)
        ojo_normal = ojo_grande(pos=(3.5, 0, 0), escala=1.0, iris=WHITE)

        self.play(FadeIn(protagonista_obj))
        self.play(FadeIn(ojo_normal))
        self.wait(0.5)
        self.play(Transform(ojo_normal, ojo_distorsionado))

        callout_text = callout("Nuestra visión no es un espejo perfecto de la realidad.", color=WHITE)
        self.play(FadeIn(callout_text))

        self.wait(3)
        self.play(FadeOut(callout_text), FadeOut(protagonista_obj), FadeOut(ojo_normal))