from manim import *
from zenn_rig import *

class S06(Scene):
    def construct(self):
        call = callout("¡CAMBIA TODO!", color=ORANGE)
        call.to_edge(UP, buff=0.55)

        prota = protagonista(pos=LEFT * 4.6 + DOWN * 0.5, playera="azul",
                             altura=3.0, expresion="sorpresa", pose="senalando")

        ojo = ojo_grande(pos=RIGHT * 4.4 + DOWN * 0.2, escala=0.9)

        f = lambda x: 0.12 * x ** 3 - 0.04
        linea = Line(LEFT * 2.0 + DOWN * 1.0, RIGHT * 2.0 + DOWN * 1.0,
                     color=INK, stroke_width=7)
        grafica = FunctionGraph(f, x_range=[-2, 2], color=RED, stroke_width=7)
        punto = Dot(grafica.get_end(), radius=0.11, color=RED)

        self.play(FadeIn(call), run_time=0.8)
        self.play(FadeIn(prota), FadeIn(ojo), run_time=0.7)
        self.wait(0.3)
        self.play(Transform(linea, grafica), run_time=1.2)
        self.play(FadeIn(punto), run_time=0.4)
        self.wait(1.0)