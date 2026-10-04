from manim import *
from zenn_rig import *

class S07(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # Fondo nocturno
        # ------------------------------------------------------------------
        self.add(fondo(INK))
        self.add(estrellas(n=30, seed=7, color=WHITE))
        self.add(luna(pos=LEFT * 5 + UP * 2, radio=1.0, color=YELLOW, bg=INK))

        # ------------------------------------------------------------------
        # Personaje narrador (monigote)
        # ------------------------------------------------------------------
        narr = stick_idle(pos=LEFT * 3, height=2.2, color=WHITE)
        self.play(FadeIn(narr, shift=RIGHT))
        # la expresión no es una animación, se añade directamente
        self.add(expresion(narr, "sorpresa"))

        # ------------------------------------------------------------------
        # Representación abstracta del cerebro (curva)
        # ------------------------------------------------------------------
        cerebro = curva(
            pos=RIGHT * 2,
            ancho=5.2,
            alto=2.8,
            color=TEAL,
            acento=RED,
        )
        self.play(FadeIn(cerebro, shift=LEFT))

        # ------------------------------------------------------------------
        # Señalar la curva con el monigote
        # ------------------------------------------------------------------
        self.play(stick_point(narr, cerebro))

        # ------------------------------------------------------------------
        # Flecha y llamado de atención
        # ------------------------------------------------------------------
        # arrow necesita coordenadas, no los objetos directamente
        flecha = arrow(
            start=narr.get_center(),
            end=cerebro.get_center(),
            color=INK,
            width=8,
        )
        llamado = callout("12+ sentidos", color=YELLOW, font_size=96)
        self.play(FadeIn(flecha), FadeIn(llamado, shift