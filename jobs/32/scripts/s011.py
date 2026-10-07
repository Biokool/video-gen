from manim import *
from zenn_rig import *

class S011(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3, playera=PLAYERA_AZUL, altura=2.6, expresion='normal', pose='de_pie')
        cambiar_cara(prota, 'sorpresa')
        self.add(prota)

        alert = callout(">300 mOsm/kg", color=ORANGE, font_size=48, pos=RIGHT*3+UP*1)
        self.add(alert)

        icon = caja(etiqueta="", pos=RIGHT*3+DOWN*1, width=0.6)
        accent = red_accent(icon, scale=1.5)
        self.add(accent)

        self.play(FadeIn(prota), run_time=0.5)
        self.play(FadeIn(alert), run_time=0.5)
        self.play(FadeIn(accent), run_time=0.5)
        self.wait(10)