from manim import *
from zenn_rig import *

class S08(Scene):
    def construct(self):
        # Fondo y horizonte
        horizon = Line(LEFT * 6, RIGHT * 6, color=WHITE).shift(DOWN * 1)
        self.play(FadeIn(horizon, shift=UP, scale=0.8))

        # Monigote inicial
        stick = stick_idle(LEFT * 5 + UP * 1.5)
        self.play(FadeIn(stick, shift=RIGHT))

        # Pequeña pausa antes de caminar
        self.wait(0.8)

        # Primera mitad del cruce (caminar)
        self.play(stick_walk(stick, RIGHT * 2, run_time=5.0))
        self.wait(0.5)

        # Callout corto al cruzar el "horizonte"
        hint = callout("Cambio de roles", color=ORANGE, font_size=96)
        hint.next_to(stick, UP, buff=0.3)
        self.play(FadeIn(hint, scale=0.5))
        self.wait(1.2)
        self.play(FadeOut(hint))

        # Continuar el cruce hasta el otro lado
        self.play(stick_walk(stick, RIGHT * 5, run_time=5.0))
        self.wait(0.8)

        # Salida de la escena
        self.play(FadeOut(stick, shift=LEFT), FadeOut(horizon, shift=DOWN))
        self.wait(0.5)