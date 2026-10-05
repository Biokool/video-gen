from manim import *
from zenn_rig import *

class S15(Scene):
    def construct(self):
        prota_a = version_prota(2, pos=LEFT * 3.7, altura=3.0)
        prota_b = version_prota(2, pos=LEFT * 3.7, altura=3.0)
        cambiar_cara(prota_b, "triste")
        ojo = ojo_grande(pos=RIGHT * 3.3 + UP * 0.5, escala=1.2, iris=TEAL)
        detalles = VGroup(*[
            Dot([x, y, 0], radius=0.15, color=ORANGE)
            for x, y in [(-1.5, 1.3), (-0.4, 0.4), (0.7, 1.5), (1.5, -0.4)]
        ])
        call = callout("¡Se pierde!", color=ORANGE, font_size=96)
        call.move_to(UP * 2.7)

        self.play(FadeIn(prota_a, shift=UP * 0.4), FadeIn(ojo), run_time=0.7)
        self.play(Write(detalles), run_time=0.6)
        self.play(
            Transform(prota_a, prota_b),
            FadeOut(detalles, shift=DOWN * 0.8),
            run_time=0.8,
        )
        self.play(FadeIn(call, shift=DOWN * 0.3), run_time=0.5)
        self.wait(0.4)