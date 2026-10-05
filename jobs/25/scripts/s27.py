from manim import *
from zenn_rig import *

class S27(Scene):
    def construct(self):
        # Personaje principal (EL PORQUÉ) con playera azul y expresión de sorpresa
        chico = protagonista(
            pos=LEFT * 3.2,
            playera="azul",
            altura=2.6,
            expresion="sorpresa",
            pose="de_pie"
        )

        # Gran ojo observador
        ojo = ojo_grande(pos=RIGHT * 3.2, escala=1.0)

        # Símbolos y caracteres abstractos flotando
        simbolos = VGroup(
            Text("?", font_size=44, color=TEAL).move_to(UP * 2.0 + LEFT * 1.0),
            Text("∀", font_size=44, color=ORANGE).move_to(UP * 1.7 + RIGHT * 0.8),
            Text("∑", font_size=44, color=RED).move_to(UP * 0.8 + RIGHT * 1.9),
            Text("@", font_size=44, color=BLUE).move_to(UP * 1.3 + LEFT * 2.2),
        )

        # Único callout corto (usa el tamaño de fuente por defecto del rig)
        idea = callout("Idioma visual", color=ORANGE)
        idea.move_to(UP * 2.8)

        # Entradas compactas y movimientos simultáneos
        self.play(
            FadeIn(chico),
            Create(ojo),
            run_time=0.8
        )
        self.play(
            FadeIn(simbolos),
            FadeIn(idea),
            run_time=0.8
        )
        self.play(
            simbolos[0].animate.shift(UP * 0.4),
            simbolos[1].animate.shift(RIGHT * 0.3),
            simbolos[2].animate.shift(UP * 0.2),
            simbolos[3].animate.shift(LEFT * 0.3),
            run_time=0.9
        )
        self.wait(0.5)