# s20.py
from manim import *
from zenn_rig import *

class S20(Scene):
    def construct(self):
        # Fondo nocturno
        self.add(fondo(INK))

        # Personaje preocupado a la izquierda
        fig = stick_idle(pos=LEFT * 3, height=2.2, color=WHITE)
        expresion(fig, "preocupado")

        # Planeta (cerebro) a la derecha
        brain = planeta(pos=RIGHT * 3, radio=0.8, color=CORAL)

        # Curva que conecta al personaje con el planeta
        conn = curva(pos=ORIGIN, ancho=5.2, alto=2.8, color=INK, acento=RED)

        # Flecha que señala la curva
        arr = arrow(fig.get_center(), conn.get_center(), color=INK, width=8)

        # Llamado de atención (callout) sobre el planeta
        call = callout("Dolor", color=ORANGE, font_size=96).move_to(brain.get_top())

        # Animaciones de aparición
        self.play(FadeIn(fig), FadeIn(brain), FadeIn(conn), FadeIn(arr), FadeIn(call))
        self.wait(2)

        # El personaje camina hacia el planeta mientras piensa
        target_pos = brain.get_center() + LEFT * 1.5
        self.play(stick_walk(fig, target=target_pos, run_time=3.0))
        self.play(stick_think(fig, "¿Qué pasa?"))
        self.wait(2)

        # Desvanecimiento final
        self.play(FadeOut(VGroup(fig, brain, conn, arr, call)))
        self.wait(1)