from manim import *
from zenn_rig import *


class S14(Scene):
    def construct(self):
        self.add(fondo(INK))

        est = estrellas(n=48, seed=3, color=WHITE)
        lu = luna(pos=LEFT * 4.6 + UP * 2.5, radio=0.75, color=YELLOW, bg=INK)
        self.play(FadeIn(est), FadeIn(lu), run_time=1.2)

        prota = protagonista(
            pos=DOWN * 1.4 + LEFT * 3.6,
            playera="verde",
            altura=2.5,
            expresion="pensando",
            pose="de_pie",
        )
        self.play(FadeIn(prota, shift=UP * 0.4), run_time=1.0)

        astro = stick_idle(pos=DOWN * 1.3 + RIGHT * 1.8, height=2.1, color=WHITE)
        instr = lupa(pos=DOWN * 0.6 + RIGHT * 3.6, escala=0.9, color=YELLOW)
        self.play(FadeIn(astro), FadeIn(instr), run_time=1.0)

        flecha = arrow(
            start=DOWN * 0.4 + RIGHT * 2.1,
            end=UP * 1.4 + RIGHT * 3.3,
            color=YELLOW,
            width=6,
        )
        self.play(Create(flecha), run_time=0.9)
        self.wait(0.4)

        dato = callout(
            "s. XII: Al-Battani midio la oblicuidad de la ecliptica con mas precision que Ptolomeo",
            color=ORANGE,
            pos=RIGHT * 3.6 + UP * 2.4,
        )
        self.play(FadeIn(dato, shift=UP * 0.3), run_time=1.2)

        cambiar_cara(prota, "sorpresa")
        self.wait(2.0)