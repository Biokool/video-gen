from manim import *
from zenn_rig import *

class S21(Scene):
    def construct(self):
        self.add(fondo(WHITE))

        prota = protagonista(pos=LEFT * 3.2 + DOWN * 0.2, playera="roja",
                             altura=3.0, expresion="pensando", pose="senalando")
        celula = ojo_grande(pos=RIGHT * 3.0 + UP * 0.6, escala=1.4, iris=TEAL)
        lab = matraz(pos=RIGHT * 3.4 + DOWN * 1.0, escala=0.9, liquido=CORAL)

        lab_etq = etiqueta("célula", (3.0, 2.2), color=INK, font_size=36)

        self.play(FadeIn(prota, shift=UP * 0.3), run_time=0.7)
        self.play(FadeIn(celula, scale=0.5), FadeIn(lab), run_time=0.6)
        self.add(lab_etq)
        self.wait(0.1)

        cambiar_cara(prota, "sorpresa")
        self.play(Create(arrow(prota.get_top() + RIGHT * 0.6,
                        celula.get_left() + LEFT * 0.3,
                        color=INK)), run_time=0.7)

        co = callout("¡Microscopio!", color=ORANGE, font_size=80)
        co.shift(UP * 2.6 + RIGHT * 0.5)
        self.play(FadeIn(co, shift=UP * 0.4), run_time=0.5)
        self.wait(0.4)