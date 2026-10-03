from manim import *
from zenn_rig import *


class S04(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(100))

        fig = stick_idle([-3.5, -1.5, 0], color=WHITE)
        self.play(FadeIn(fig), run_time=1.5)
        self.add(expresion(fig, "preocupado"))

        thought1 = stick_think(fig, "Galaxias")
        self.play(FadeIn(thought1), run_time=2.5)
        self.wait(0.5)

        sun = sol()
        sun.move_to([0.5, 2.5, 0])
        self.play(Create(sun), run_time=1.0)

        earth = planeta([2.0, 1.0, 0], 0.2, TEAL)
        neptune = planeta([4.0, -0.5, 0], 0.28, RED)
        self.play(FadeIn(earth), FadeIn(neptune), run_time=1.0)

        c1 = callout("Cerca: rápido", ORANGE, 48)
        c1.move_to([-2.5, 2.5, 0])
        self.play(FadeIn(c1), run_time=0.8)

        a1 = arrow([2.2, 1.0, 0], [3.0, 1.0, 0])
        self.play(Create(a1), run_time=0.5)

        self.wait(0.5)

        c2 = callout("Lejos: lento", RED, 48)
        c2.move_to([2.5, -2.2, 0])
        self.play(FadeIn(c2), run_time=0.8)

        a2 = arrow([4.2, -0.5, 0], [5.0, -0.5, 0])
        self.play(Create(a2), run_time=0.5)

        self.wait(0.5)

        thought2 = stick_think(fig, "¿Materia oscura?")
        self.play(FadeIn(thought2), run_time=2.5)
        self.wait(2.4)