from manim import *
from zenn_rig import *

class S21(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=42, seed=7, color=WHITE))

        fig = stick_idle(pos=LEFT * 4, height=2.2, color=WHITE)
        self.add(fig)
        self.add(expresion(fig, tipo="sorpresa"))

        onda = curva(pos=RIGHT * 3, ancho=5.2, alto=2.8, color=WHITE, acento=RED)
        self.play(Create(onda), run_time=1.5)

        aviso = callout("Ondas sensibles", color=YELLOW, font_size=96)
        aviso.to_edge(UP, buff=0.5)
        self.play(FadeIn(aviso), run_time=1.0)

        puntero = stick_point(fig, onda.get_center())
        if isinstance(puntero, Animation):
            self.play(puntero, run_time=1.5)
        elif isinstance(puntero, Mobject):
            self.play(FadeIn(puntero), run_time=1.5)
        else:
            self.wait(1.5)

        self.wait(2.0)