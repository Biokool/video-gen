from manim import *
from zenn_rig import *

class S02(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=42, seed=7, color=WHITE))

        protagonista_obj = protagonista(pos=ORIGIN, playera=PLAYERA_NARANJA, altura=3.0, expresion='pensando', pose='de_pie')
        ojo_grande_obj = ojo_grande(pos=protagonista_obj.get_center() + UP * 1.5, escala=1.5, iris=YELLOW)

        flecha_abajo = arrow(start=protagonista_obj.get_center() + DOWN * 0.5, end=protagonista_obj.get_center() + DOWN * 2.0, color=WHITE, width=8)
        flecha_arriba = arrow(start=protagonista_obj.get_center() + UP * 0.5, end=protagonista_obj.get_center() + UP * 2.0, color=WHITE, width=8)

        callout_texto = "El mundo a diferentes escalas..."
        callout_obj = callout(callout_texto, color=ORANGE, font_size=72)
        callout_obj.next_to(protagonista_obj, UP, buff=1.0)

        self.play(FadeIn(protagonista_obj), FadeIn(ojo_grande_obj))
        self.play(Create(flecha_abajo), Create(flecha_arriba))
        self.play(Write(callout_obj))
        self.wait(4)

        self.play(FadeOut(protagonista_obj), FadeOut(ojo_grande_obj), FadeOut(flecha_abajo), FadeOut(flecha_arriba), FadeOut(callout_obj))
        self.wait(1)