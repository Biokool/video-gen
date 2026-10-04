from manim import *
from zenn_rig import *

class S10(Scene):
    def construct(self):
        # --------------------------------------------------------------------
        # Fondo claro
        # --------------------------------------------------------------------
        self.add(fondo(WHITE))

        # --------------------------------------------------------------------
        # Protagonista “EL PORQUÉ” (versión azul) y elementos auxiliares
        # --------------------------------------------------------------------
        prota = version_prota(2, pos=LEFT * 3)                # versión azul
        ojo = ojo_grande(pos=RIGHT * 2, escala=1.2)          # ojo grande como foco
        etiqueta_vis = etiqueta(
            "Agudeza Visual",
            (RIGHT * 2 + DOWN * 0.6),
            color=INK,
            font_size=40,
            ancho_max=5.5,
        )
        narr = callout(
            "Agudeza Visual",
            color=ORANGE,
            font_size=96,
        )

        # --------------------------------------------------------------------
        # Entrada de los elementos
        # --------------------------------------------------------------------
        self.play(
            FadeIn(prota),
            FadeIn(ojo),
            FadeIn(etiqueta_vis),
        )
        self.wait(0.8)

        # --------------------------------------------------------------------
        # Cambiar expresión del protagonista (no es una animación)
        # --------------------------------------------------------------------
        cambiar_cara(prota, "pensando")          # expresión pensativa
        self.wait(1.5)

        # --------------------------------------------------------------------
        # Mostrar el callout y señalar con una flecha
        # --------------------------------------------------------------------
        self.play(FadeIn(narr))
        self.wait(0.5)

        flecha = arrow(
            start=ojo.get_center(),
            end=etiqueta_vis.get_center(),
            color=INK,
            width=8,
        )
        self.play(Create(flecha))
        self.wait(0.5)

        # --------------------------------------------------------------------
        # Resaltar el ojo con un acento rojo
        # --------------------------------------------------------------------
        # red_accent devuelve un Mobject (un círculo rojo). Lo introducimos con FadeIn.
        self.play(FadeIn(red_accent(ojo, scale=1.25)))
        self.wait(1.0)

        # --------------------------------------------------------------------
        # Salida: desvanecer todo
        # --------------------------------------------------------------------
        self.play(
            FadeOut(
                VGroup(
                    prota,
                    ojo,
                    etiqueta_vis,
                    narr,
                    flecha,
                )
            )
        )
        self.wait(0.5)