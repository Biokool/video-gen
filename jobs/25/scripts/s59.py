from manim import *
from zenn_rig import *

class S59(Scene):
    def construct(self):
        # Personaje principal "EL PORQUÉ" con playera naranja, perplejo.
        prota = protagonista(
            pos=LEFT * 3.5,
            playera="naranja",
            altura=3.0,
            expresion="pensando",
            pose="senalando"
        )

        # Ojo grande que observa, y bacteria diminuta.
        ojo = ojo_grande(pos=RIGHT * 2.0 + UP * 0.5, escala=1.0, iris=TEAL)
        bacteria = VGroup(
            Circle(radius=0.25, color=TEAL, fill_opacity=0.75, stroke_width=3),
            Line(LEFT * 0.25, LEFT * 0.9, color=TEAL, stroke_width=4),
            Line(UP * 0.25, UP * 0.7, color=TEAL, stroke_width=3),
            Line(DOWN * 0.25, DOWN * 0.7, color=TEAL, stroke_width=3),
            Line(UP * 0.25 + LEFT * 0.2, UP * 0.6 + LEFT * 0.6, color=TEAL, stroke_width=2),
        ).move_to(RIGHT * 4.5 + DOWN * 1.1)

        etiqueta_bacteria = etiqueta("bacteria", (4.5, -1.8), font_size=36)

        # Entrada rápida de los elementos.
        self.play(
            FadeIn(prota, run_time=0.5),
            FadeIn(ojo, run_time=0.5)
        )

        # La bacteria aparece: algo pequeño pero presente.
        self.play(
            Create(bacteria, run_time=0.6),
            FadeIn(etiqueta_bacteria, run_time=0.3)
        )

        # Reacción: perplejidad ante lo diminuto.
        cambiar_cara(prota, "confundido")
        self.wait(0.3)

        # Pregunta retórica corta.
        pregunta = callout("¿insignificante?", color=ORANGE, font_size=72)
        pregunta.move_to(UP * 2.7)
        self.play(FadeIn(pregunta, run_time=0.4))
        self.wait(0.7)

        self.play(
            FadeOut(pregunta),
            FadeOut(prota),
            FadeOut(ojo),
            FadeOut(bacteria),
            FadeOut(etiqueta_bacteria),
            run_time=0.3
        )