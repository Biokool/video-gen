from manim import *
from zenn_rig import *

class S20(Scene):
    def construct(self):
        # Fondo nocturno
        self.add(fondo(INK))

        # Título del segmento
        title = title_card("¿Por qué el cielo es azul?", color=YELLOW)
        self.play(FadeIn(title, scale=0.5))
        self.wait(2)
        self.play(FadeOut(title))

        # Protagonista principal (confundido, playera roja)
        prota = protagonista(
            pos=ORIGIN,
            playera="roja",
            altura=3.0,
            expresion="confundido",
            pose="de_pie",
        )
        self.play(FadeIn(prota))
        self.wait(1)

        # Monigote secundario (idle) a la izquierda
        stick = stick_idle(pos=LEFT * 4, height=2.2, color=WHITE)
        self.play(FadeIn(stick))
        self.wait(0.5)

        # Camina hacia el protagonista
        target = ORIGIN + RIGHT * 2
        self.play(stick_walk(stick, target, run_time=2.0, steps=6))
        self