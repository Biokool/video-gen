from manim import *
from zenn_rig import *

class S80(Scene):
    def construct(self):
        prota = version_prota(7, pos=LEFT * 3 + DOWN * 0.5)
        cambiar_cara(prota, "sorpresa")

        ojo = ojo_grande(pos=RIGHT * 4.5 + UP * 1.5, escala=1.0, iris=TEAL)
        celula = planeta(pos=RIGHT * 1.5 + UP * 0.5, radio=0.7, color=CORAL)
        molecula = sol(pos=RIGHT * 3.5 + DOWN * 1.0, radius=0.3, color=ORANGE)

        self.play(
            FadeIn(prota), FadeIn(ojo), FadeIn(celula), FadeIn(molecula),
            run_time=1.0
        )
        self.play(
            celula.animate.shift(RIGHT * 0.4 + UP * 0.2).rotate(PI / 6),
            molecula.animate.shift(LEFT * 0.3 + DOWN * 0.2).rotate(PI / 4),
            ojo.animate.rotate(0.2),
            run_time=1.5
        )
        self.play(
            celula.animate.shift(LEFT * 0.5 + DOWN * 0.1).rotate(-PI / 4),
            molecula.animate.shift(UP * 0.4 + RIGHT * 0.2).rotate(-PI / 3),
            ojo.animate.rotate(-0.2),
            run_time=1.5
        )
        self.play(
            celula.animate.shift(UP * 0.3 + LEFT * 0.2).rotate(PI / 5),
            molecula.animate.shift(RIGHT * 0.3 + DOWN * 0.3).rotate(PI / 2),
            run_time=1.5
        )
        self.wait(0.5)