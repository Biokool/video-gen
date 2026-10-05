from manim import *
from zenn_rig import *

class S45(Scene):
    def construct(self):
        # Fondo espacial
        self.add(fondo(INK))
        self.play(FadeIn(estrellas(n=35, seed=7)), run_time=0.6)

        # Protagonista "EL PORQUÉ" como conductor
        prota = protagonista(
            pos=DOWN * 0.8,
            playera="naranja",
            altura=3.0,
            expresion="sorpresa",
            pose="de_pie"
        )
        self.play(FadeIn(prota), run_time=0.5)

        # Monigote observando la inmensidad
        mono = stick_idle(pos=LEFT * 4.8 + DOWN * 0.6, height=2.4, color=WHITE)
        expresion(mono, "sorpresa")
        self.play(FadeIn(mono), run_time=0.5)

        # Ojo grande: asombro ante la distancia
        ojo = ojo_grande(pos=RIGHT * 3.4 + DOWN * 0.3, escala=0.9, iris=YELLOW)
        self.play(FadeIn(ojo, shift=DOWN), run_time=0.6)

        # La luz viaja: recorrido representado con una flecha
        self.play(Create(arrow(LEFT * 7 + UP * 1.5, RIGHT * 6.2 + UP * 1.5, color=YELLOW)), run_time=1.2)

        # Señala la distancia (sin pasar el resultado de stick_point a play)
        stick_point(mono, RIGHT * 6.2 + UP * 1.5)
        self.wait(0.5)

        # Etiqueta pequeña sobre la línea
        self.play(FadeIn(etiqueta("1 año luz", (0, 2.25))), run_time=0.3)
        self.wait(0.3)

        # Dato destacado en pantalla
        self.play(FadeIn(callout("¡9.46 billones de km!", color=ORANGE), shift=UP), run_time=0.6)
        self.wait(0.8)