from manim import *
from zenn_rig import *

class S14(Scene):
    def construct(self):
        est = estrellas(n=24, seed=11, color=WHITE)

        prota = protagonista(pos=(-5.0, -1.6, 0), playera="azul", altura=3.0,
                             expresion='pensando', pose='senalando')
        ojo = ojo_grande(pos=(0.5, 2.8, 0), escala=0.8, iris=TEAL)
        hormiga = pez(pos=(5.4, 0.6, 0), color=CORAL, escala=0.9)
        lab = etiqueta("silueta de color", (5.4, -1.6, 0), color=CORAL, font_size=34)
        ar = arrow((-2.6, 1.4, 0), (4.4, 0.9, 0), color=INK, width=6)

        self.play(FadeIn(est, scale=1.15), run_time=0.4)
        self.play(FadeIn(prota, shift=UP * 0.3), run_time=0.5)
        self.play(Create(ojo), run_time=0.5)
        self.play(FadeIn(hormiga, scale=0.5), run_time=0.5)
        self.play(FadeIn(lab), run_time=0.3)

        cambiar_cara(prota, 'sorpresa')

        self.play(Create(ar), FadeIn(callout("¡TIENE COLOR!", ORANGE, font_size=64)),
                  run_time=0.6)
        self.wait(0.5)