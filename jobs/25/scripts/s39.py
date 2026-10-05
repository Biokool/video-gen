from manim import *
from zenn_rig import *

class S39(Scene):
    def construct(self):
        self.add(fondo(INK))

        prota = version_prota(5, pos=LEFT * 3.5, altura=3.0)
        cambiar_cara(prota, "sorpresa")

        ojo = ojo_grande(pos=LEFT * 4.6 + UP * 1.1, escala=0.7)
        planeta_obj = planeta(pos=RIGHT * 3.2, radio=1.2, color=TEAL)

        self.play(
            FadeIn(prota, shift=UP * 0.2),
            Create(ojo),
            FadeIn(planeta_obj, shift=DOWN * 0.2),
            run_time=0.6,
        )

        self.play(Rotate(planeta_obj, angle=PI, run_time=1.0))

        pregunta = callout("¿A un planeta?", color=ORANGE).shift(UP * 1.9)
        self.play(FadeIn(pregunta), run_time=0.3)
        self.wait(0.4)