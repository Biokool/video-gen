from manim import *
from zenn_rig import *


class S13(Scene):
    def construct(self):
        prota = protagonista(LEFT * 3.6, playera="#1E88E5", altura=3.0,
                             expresion='sorpresa', pose='senalando')
        cal = calendario(RIGHT * 3.3, width=2.2)
        lbl = etiqueta("5 minutos", (3.3, 1.5), color=INK)

        self.play(FadeIn(prota, shift=RIGHT * 0.4), Create(cal), run_time=1.2)
        self.play(Write(lbl), run_time=0.8)
        self.wait(0.4)

        flecha = arrow(LEFT * 1.7 + UP * 0.3, RIGHT * 1.7 + UP * 0.3, color=INK)
        self.play(Create(flecha), run_time=0.6)

        acento = red_accent(lbl, scale=1.3)
        self.play(Create(acento), run_time=0.6)

        cambiar_cara(prota, 'mente_explotada')
        self.wait(0.5)

        co = callout("¡NO EN 5 MIN!", color=CORAL, font_size=72)
        co.move_to(UP * 2.7)
        self.play(FadeIn(co, scale=1.2), run_time=0.8)
        self.wait(1.2)

        self.play(FadeOut(co), FadeOut(flecha), FadeOut(acento), run_time=0.6)

        cambiar_cara(prota, 'decidido')
        self.wait(1.1)