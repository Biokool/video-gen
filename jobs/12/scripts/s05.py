from manim import *
from zenn_rig import *

class S05(Scene):
    def construct(self):
        # Fondo verde‑agua
        self.add(fondo(TEAL))

        # Título superior
        titulo = titulo_seguro("Clasificación incompleta", color=ORANGE)
        self.play(FadeIn(titulo, shift=UP))
        self.wait(0.8)

        # Monigote Aristóteles (túnica blanca)
        arist = stick_idle(pos=LEFT * 3, height=2.2, color=WHITE)
        self.play(FadeIn(arist, shift=RIGHT))
        self.wait(0.4)

        # Expresión de sorpresa
        cara = expresion(arist, tipo="sorpresa")
        self.play(FadeIn(cara))
        self.wait(0.4)

        # Etiqueta “5 sentidos” sobre su cabeza
        etiqueta_sentidos = etiqueta(
            "5 sentidos",
            (arist.get_center()[0], arist.get_center()[1] + 1.5),
            color=INK,
            font_size=40,
        )
        self.play(FadeIn(etiqueta_sentidos, shift=UP))
        self.wait(0.4)

        # Limpieza y final
        self.play(FadeOut(VGroup(titulo, arist, cara, etiqueta_sentidos)))
        self.wait(1)