from manim import *
from zenn_rig import *


class S07(Scene):
    def construct(self):
        titulo = banda_titulo("5 minutos de 'om'", color=AZUL_MARINO)
        prota = protagonista(pos=LEFT * 3.2 + DOWN * 0.4, playera=AZUL_MARINO,
                             expresion='sorpresa', pose='de_pie')
        nube = callout("estrés", color=RED, font_size=72).move_to(RIGHT * 2.9 + UP * 0.6)

        self.play(FadeIn(titulo), FadeIn(prota), FadeIn(nube, scale=0.5), run_time=1.2)
        self.wait(0.6)

        zas = callout("¡ZAS!", color=YELLOW, font_size=110).move_to(RIGHT * 2.9 + UP * 0.6)
        cambiar_cara(prota, 'mente_explotada')
        self.play(Transform(nube, zas), run_time=1.0)
        self.wait(0.5)

        self.play(FadeOut(nube), run_time=0.7)
        cambiar_cara(prota, 'alegria_pura')
        self.wait(0.3)
        self.play(FadeOut(titulo), FadeOut(prota), run_time=0.9)