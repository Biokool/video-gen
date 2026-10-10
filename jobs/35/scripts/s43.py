from manim import *
from zenn_rig import *

class S43(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_NARANJA, altura=2.6, expresion='feliz', pose='de_pie')
        self.play(FadeIn(prota), run_time=1.0)
        self.wait(0.5)
        new_prota = cambiar_cara(prota, 'pensando')
        self.play(Transform(prota, new_prota), run_time=0.5)
        self.wait(0.5)
        dato = callout(text="¿Sabías que el día tiene 24 horas por la rotación de la Tierra?", color=ORANGE, pos=RIGHT*3.4+UP*1)
        self.play(FadeIn(dato), run_time=1.0)
        self.wait(1.0)