from manim import *
from zenn_rig import *

class S17(Scene):
    def construct(self):
        # Fondo nocturno (negro)
        self.add(fondo(INK))

        # Banda superior con título
        titulo = banda_titulo(
            "EL MURMULLO INTERNO: LA INTEROCEPCIÓN",
            color=TEAL,
        )
        self.play(FadeIn(titulo, shift=UP))
        self.wait(1)

        # Monigote que llega caminando
        stick = stick_idle(pos=LEFT * 7, height=2.2, color=WHITE)
        self.play(FadeIn(stick, shift=RIGHT))
        self.play(stick_walk(stick, LEFT * 2, run_time=2.0))
        self.play(expresion(stick, tipo="preocupado"))
        self.wait(0.5)

        # Caja que representa la ansiedad
        caja_ans = caja("Ansiedad", pos=RIGHT * 4 + DOWN * 0.5, width=2)
        self.play(FadeIn(caja_ans, shift=LEFT))
        self.wait(0.5)

        # El monigote señala la caja y piensa
        self.play(stick_point(stick, caja_ans))
        self.play(stick_think(stick, "¿Cómo calmarla?"))
        self.wait(1)

        # Llamado a la acción con flecha
        llamado = callout("Respira", color=ORANGE, font_size=96)
        self.play(FadeIn(llamado, shift=UP))
        flecha = arrow(stick.get_center(), llamado.get_center())
        self.play(FadeIn(flecha, shift=UP))
        self.wait(1)

        # Salida
        self.play(FadeOut(VGroup(titulo, stick, caja_ans, llamado, flecha)))
        self.wait(1)