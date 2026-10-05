from manim import *
from zenn_rig import *

class S62(Scene):
    def construct(self):
        self.add(fondo(INK))

        pro = protagonista(
            pos=LEFT * 3.2,
            playera="verde",
            altura=3.0,
            expresion="sorpresa",
            pose="senalando"
        )
        ojo = ojo_grande(pos=LEFT * 6.2, escala=0.8, iris=GREEN)

        escala = arrow(
            start=LEFT * 5.6,
            end=RIGHT * 5.6,
            color=WHITE,
            width=8
        ).shift(UP * 2.3)

        etiq_izq = etiqueta("átomos", (-5.4, 2.9), color=WHITE)
        etiq_der = etiqueta("galaxias", (5.4, 2.9), color=WHITE)

        self.play(FadeIn(pro), FadeIn(ojo), run_time=0.8)
        self.wait(0.3)

        self.play(Create(escala), run_time=1.2)
        self.play(FadeIn(etiq_izq), FadeIn(etiq_der), run_time=0.7)
        self.wait(0.5)

        cambiar_cara(pro, "mente_explotada")
        self.wait(1.5)