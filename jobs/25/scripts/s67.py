from manim import *
from zenn_rig import *

class S67(Scene):
    def construct(self):
        fondo_oscuro = fondo(INK)
        self.add(fondo_oscuro)

        estrellas_grp = estrellas(n=42, seed=7, color=WHITE)
        self.add(estrellas_grp)

        prota = protagonista(
            pos=LEFT * 2.5 + DOWN * 0.6,
            playera="naranja",
            expresion="sorpresa",
            pose="de_pie"
        )
        self.play(FadeIn(prota, shift=UP), run_time=0.8)

        ojo = ojo_grande(pos=RIGHT * 3.0 + UP * 0.3, escala=2.8, iris=TEAL)
        self.play(FadeIn(ojo, shift=LEFT), run_time=0.8)

        cosmic = callout("PERSPECTIVA CÓSMICA", color=YELLOW, font_size=48)
        cosmic.move_to(UP * 2.6)
        self.play(Write(cosmic), run_time=1.0)

        self.play(estrellas_grp.animate.scale(1.5), run_time=2.0)
        self.wait(0.5)