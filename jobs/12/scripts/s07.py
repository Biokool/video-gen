from manim import *
from zenn_rig import *

class S07(Scene):
    def construct(self):
        # Fondo nocturno
        self.add(fondo(INK))
        self.add(estrellas(n=30, seed=7, color=WHITE))
        self.add(luna(pos=LEFT * 5 + UP * 2, radio=1.0, color=YELLOW, bg=INK))

        # Personaje narrador (monigote)
        narr = stick_idle(pos=LEFT * 3, height=2.2, color=WHITE)
        self.play(FadeIn(narr, shift=RIGHT))
        # la expresión no es una animación, se añade directamente
        self.add(expresion(narr, "sorpresa"))

        # Representación abstracta del cerebro (curva)
        cerebro = curva(
            pos=RIGHT * 2 + DOWN * 0.5,
            ancho=5.2,
            alto=2.8,
            color=TEAL,
            acento=RED,
        )
        self.play(FadeIn(cerebro, shift=LEFT))

        # Señalar la curva: point() muta el brazo en el acto (no es animación)
        # y recibe una coordenada, no el objeto.
        narr.point(RIGHT * 2 + DOWN * 0.5)
        self.wait(0.6)

        # Flecha y llamado de atención
        # (flecha WHITE: sobre fondo INK la INK sería invisible)
        flecha = arrow(
            start=narr.get_center(),
            end=cerebro.get_center(),
            color=WHITE,
            width=8,
        )
        llamado = callout("12+ sentidos", color=YELLOW, font_size=72)
        llamado.move_to(UP * 3.05)
        self.play(FadeIn(flecha), FadeIn(llamado, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(flecha), FadeOut(llamado))
        self.wait(0.5)
