from manim import *
from zenn_rig import *

class S05(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=42, seed=7, color=WHITE))

        protagonista_principal = version_prota(1, pos=DOWN*1.2+LEFT*3.5)
        self.play(FadeIn(protagonista_principal))

        adn_obj = adn(pos=ORIGIN, escala=0.8, color=TEAL)

        self.play(FadeIn(adn_obj, shift=UP))
        self.wait(1)

        callout_text = "No hay un único gen del zurdo o diestro."
        callout_obj = callout(callout_text, color=ORANGE, pos=RIGHT*3.4+UP*1)
        self.play(FadeIn(callout_obj))
        self.wait(3)

        self.play(FadeOut(callout_obj), FadeOut(adn_obj))
        self.play(FadeOut(protagonista_principal))
        self.wait(1)