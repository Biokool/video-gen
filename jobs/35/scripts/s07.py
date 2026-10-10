from manim import *
from zenn_rig import *

class S07(Scene):
    def construct(self):
        # Fondo
        self.add(fondo(CREMA))

        # Título de la escena
        banda = banda_titulo("Una decisión previa", color=ORANGE)
        self.play(FadeIn(banda, shift=DOWN))
        self.wait(0.5)

        # Protagonista (versión 5 = pregunta amarilla)
        prota = version_prota(
            5,
            pos=DOWN * 1.2 + LEFT * 3.0,
            altura=2.6,
        )
        self.play(FadeIn(prota, shift=UP))
        self.wait(0.5)

        # Ojo grande (feto) – se escala antes de la animación
        feto = ojo_grande(
            pos=UP * 0.5 + RIGHT * 1.5,
            escala=1.2,
            iris=ORANGE,
        )
        feto.scale(0.5)                     # escala correcta antes de la animación
        self.play(FadeIn(feto))
        self.wait(0.5)

        # Monigote secundario
        stick = stick_idle(
            pos=RIGHT * 4.5 + DOWN * 0.5,
            height=1.8,
            color=INK,
        )
        self.play(FadeIn(stick))
        self.wait(0.5)

        # Cambio de expresión del protagonista
        cambiar_cara(prota, "sorpresa")
        self.wait(0.5)

        # Texto secundario (etiqueta)
        etiqueta_txt = etiqueta(
            "Antes de que existieras",
            pos=RIGHT * 3.2 + UP * 1.2,
            color=ORANGE,
            font_size=40,
            ancho_max=5.5,
        )
        self.play(FadeIn(etiqueta_txt))
        self.wait(0.5)

        # El monigote señala al ojo grande
        # stick_point necesita la posición del objetivo, no el Mobject
        stick_point(stick, feto.get_center())
        self.wait(0.8)

        # Fin de la escena
        self.wait(1)