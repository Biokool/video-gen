from manim import *
from zenn_rig import *

class S101(Scene):
    def construct(self):
        fondo(INK)
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_NARANJA, altura=2.6, expresion='feliz', pose='de_pie')
        self.add(prota)
        self.wait(2)
        callout_text = "¡Suscríbete para más respuestas!"
        callout_obj = callout(callout_text, color=ORANGE, font_size=60, ancho_max=7.0, pos=RIGHT*3.4+UP*1)
        self.play(FadeIn(callout_obj))
        self.wait(4)
        self.play(FadeOut(callout_obj))
        self.wait(2)
        self.play(FadeOut(prota))
        self.wait(6)