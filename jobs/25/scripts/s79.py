from manim import *
from zenn_rig import *

class S79(Scene):
    def construct(self):
        self.add(fondo(WHITE))

        # Protagonista con playera naranja, en actitud de agradecimiento
        por = protagonista(
            LEFT * 3,
            playera="naranja",
            altura=3.0,
            expresion="feliz",
            pose="de_pie"
        )
        self.play(FadeIn(por, shift=DOWN * 0.4), run_time=0.7)

        # Herramientas científicas que aparecen como regalos
        ojo = ojo_grande(
            pos=RIGHT * 2.6 + UP * 0.7,
            escala=1.1,
            iris=TEAL
        )
        matraz_objeto = matraz(
            pos=RIGHT * 2.6 + DOWN * 0.6,
            escala=1.1,
            liquido=TEAL
        )
        self.play(
            FadeIn(ojo, shift=UP * 0.5),
            FadeIn(matraz_objeto, shift=DOWN * 0.5),
            run_time=0.8
        )

        # Reacción de gratitud y leve flotación de regalos
        cambiar_cara(por, "alegria_pura")
        self.play(
            ojo.animate.shift(UP * 0.25),
            matraz_objeto.animate.shift(UP * 0.25),
            run_time=0.6
        )

        self.wait(0.8)