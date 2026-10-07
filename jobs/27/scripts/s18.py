from manim import *
from zenn_rig import *


class S18(Scene):
    def construct(self):
        self.add(fondo_papel())
        banda = banda_titulo("Una ruptura conceptual", color=RED)
        self.play(FadeIn(banda, shift=DOWN * 0.3), run_time=0.7)

        prota = protagonista(DOWN * 1.5 + LEFT * 3.6, playera="roja", altura=2.6,
                             expresion="pensando", pose="de_pie")
        self.play(FadeIn(prota, shift=UP * 0.4), run_time=0.8)
        self.wait(0.3)

        idea = matraz(LEFT * 0.4 + DOWN * 1.3, escala=1.15, liquido=TEAL)
        self.play(Create(idea), run_time=1.0)
        self.wait(0.4)

        esp1 = adn(RIGHT * 0.9 + UP * 0.7, escala=0.38, color=TEAL)
        esp2 = adn(RIGHT * 1.9 + DOWN * 0.6, escala=0.30, color=AZUL_MARINO)
        self.play(FadeIn(esp1, scale=0.5), FadeIn(esp2, scale=0.5), run_time=0.8)

        cambiar_cara(prota, "sorpresa")
        self.play(Indicate(prota, scale_factor=1.05), run_time=0.9)
        self.wait(0.5)

        aviso = etiqueta("Aún imperfecto", RIGHT * 4.2 + UP * 1.3, color=RED, font_size=40)
        self.play(FadeIn(aviso, shift=LEFT * 0.3), run_time=0.8)
        self.wait(0.7)

        self.play(FadeOut(esp1), FadeOut(esp2), run_time=0.9)
        self.play(Indicate(idea, color=RED, scale_factor=1.18), run_time=0.7)

        cambiar_cara(prota, "feliz")
        self.wait(1.3)