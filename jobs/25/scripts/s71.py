from manim import *
from zenn_rig import *

class S71(Scene):
    def construct(self):
        # Protagonista con playera naranja, expresión de ingenio y señalando
        prota = protagonista(
            pos=LEFT * 3.2,
            playera=PLAYERA_NARANJA,
            altura=3.0,
            expresion='sarcastico',
            pose='senalando'
        )

        # El ojo que se convertirá en dispositivo
        ojo = ojo_grande(pos=RIGHT * 3.2, escala=1.2, iris=TEAL)

        # Entrada
        self.play(FadeIn(prota, shift=UP * 0.3), FadeIn(ojo, shift=DOWN * 0.3))
        self.wait(0.5)

        # El dispositivo tecnológico (caja etiquetada)
        dispositivo = caja("TEC", pos=RIGHT * 3.2, width=1.8)

        # Un ojo se transforma en dispositivo
        self.play(
            Transform(ojo, dispositivo),
            run_time=1.8
        )

        # Callout corto
        sufijo = callout("EXTENSIONES", color=ORANGE, font_size=60)
        sufijo.to_edge(UP, buff=0.8)
        self.play(Write(sufijo), run_time=0.7)
        self.wait(1.0)

        # Cierre limpio
        self.play(
            FadeOut(prota),
            FadeOut(ojo),
            FadeOut(sufijo),
            run_time=0.8
        )
        self.wait(0.4)