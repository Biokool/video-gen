from manim import *
from zenn_rig import *

class S036(Scene):
    def construct(self):
        # protagonista
        prota = protagonista(pos=LEFT*7, playera="roja", altura=2.6, expresion="pensando", pose="de_pie")
        final_pos = LEFT*4 + DOWN*0.5
        self.play(FadeIn(prota), prota.animate.move_to(final_pos), run_time=1.5)
        self.wait(0.5)

        # callout: porcentaje de disminución
        percent = callout("10‑20% ↓", color=ORANGE)
        percent.move_to(RIGHT*4 + UP*2)
        self.play(FadeIn(percent), run_time=1)
        self.wait(0.5)

        # etiqueta: referencia del estudio
        study = etiqueta("Popkin et al., 2010", RIGHT*4, color=INK, font_size=40)
        study.move_to(RIGHT*4 + DOWN*0.5)
        self.play(FadeIn(study), run_time=1)
        self.wait(0.5)

        # cambio de expresión para enfatizar el dato
        cambiar_cara(prota, "sorpresa")
        self.wait(1.5)
        cambiar_cara(prota, "pensando")
        self.wait(1.5)

        # salida
        self.play(FadeOut(prota), FadeOut(percent), FadeOut(study), run_time=1)
        self.wait(0.5)