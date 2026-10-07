from manim import *
from zenn_rig import *

class S09(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3.5 + DOWN*0.5, playera=PLAYERA_AZUL, altura=2.6, expresion='pensando', pose='de_pie')
        drop = moneda_dorada(texto='', pos=RIGHT*3.5 + UP*0.5, radio=0.2)
        drop.set_color(RED)
        label = etiqueta("osmolaridad_subiendo", pos=RIGHT*3.5 + UP*1.5, color=INK, font_size=40)

        self.play(FadeIn(prota), run_time=1.5)
        self.play(FadeIn(drop), run_time=1.5)
        self.play(Write(label), run_time=1.5)
        self.wait(3)