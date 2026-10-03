from manim import *
from zenn_rig import *

class S07(Scene):
    def construct(self):
        # Grupo de 3 monigotes
        grupo = stick_group(3, center=LEFT * 4, spacing=1.5, height=2.0)
        self.play(FadeIn(grupo, scale=0.5))
        self.wait(1)

        # Posiciones objetivo para cada monigote
        objetivos = [
            RIGHT * 6,
            RIGHT * 6 + UP * 0.5,
            RIGHT * 6 + DOWN * 0.5,
        ]

        # Cada monigote camina hacia su objetivo
        for fig, meta in zip(grupo, objetivos):
            self.play(stick_walk(fig, meta, run_time=2.0))
        self.wait(2)

        # Llamada breve al tema
        llamado = callout("Red cósmica", color=ORANGE, font_size=48)
        llamado.move_to(UP * 2)
        self.play(FadeIn(llamado, scale=0.5))
        self.wait(1)
        self.play(FadeOut(llamado))

        self.wait(2)