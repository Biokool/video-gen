from manim import *
from zenn_rig import *

class S13(Scene):
    def construct(self):
        self.play(FadeIn(fondo(INK)))

        self.add(titulo_seguro("Cascos de Veksø"))

        cascos = casco_vikingo(pos=RIGHT * 3 + UP * 0.5, escala=1.4)
        self.play(
            FadeIn(cascos, shift=0.5 * RIGHT),
            run_time=0.8
        )

        self.play(
            Create(red_accent(cascos)),
            run_time=0.5
        )

        self.add(etiqueta("Hallados en Dinamarca", UP * 1.5 + LEFT * 2.5, color=YELLOW, font_size=40))

        prota = version_prota(6, pos=LEFT * 4 + DOWN * 1.5, altura=2.4)
        self.play(
            FadeIn(prota, shift=0.3 * DOWN),
            run_time=1.0
        )

        self.wait(1.0)

        self.play(
            FadeOut(cascos),
            FadeOut(prota),
            run_time=0.8
        )