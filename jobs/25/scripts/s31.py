from manim import *
from zenn_rig import *

class S31(Scene):
    def construct(self):
        # Protagonista con playera rosa, incredulidad
        p = protagonista(LEFT * 3.5 + DOWN * 0.3, playera='rosa', expresion='sorpresa', pose='de_pie')
        self.play(FadeIn(p))
        self.wait(0.3)

        # Gran ojo que enfatiza lo diminuto
        ojo = ojo_grande(RIGHT * 3.1 + UP * 0.4, escala=0.7, iris=TEAL)
        self.play(FadeIn(ojo), run_time=0.8)

        # Regla grande con etiqueta "1 m"
        regla = Line(LEFT * 2, RIGHT * 2, color=INK, stroke_width=8)
        regla.move_to(UP * 0.9)
        etiqueta_regla = etiqueta("1 m", (0, 2.0))
        self.play(Create(regla), FadeIn(etiqueta_regla), run_time=1.0)
        self.wait(0.4)

        # La regla se encoge drásticamente
        regla_pequena = Line(LEFT * 0.002, RIGHT * 0.002, color=INK, stroke_width=2)
        regla_pequena.move_to(UP * 0.9)
        etiqueta_pequena = etiqueta("1 µm = 0.000001 m", (0, 2.0))
        self.play(
            Transform(regla, regla_pequena),
            Transform(etiqueta_regla, etiqueta_pequena),
            run_time=2.0
        )
        self.wait(0.3)

        # Reacción de asombro total
        cambiar_cara(p, 'mente_explotada')
        self.wait(0.4)

        # Único callout de la escena
        call = callout("¡Diminuto!", color=ORANGE, font_size=96)
        call.to_edge(UP, buff=0.3)
        self.play(FadeIn(call), run_time=0.8)
        self.wait(1.2)