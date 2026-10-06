from manim import *
from zenn_rig import *

class S06(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2+LEFT*4, playera="azul", altura=2.6, expresion="mente_explotada", pose="senalando")
        bar_blue = caja("Luz azul", pos=LEFT*2+UP*0.5, width=2.0)
        bar_blue.set_color(BLUE)
        bar_red = caja("Luz roja", pos=RIGHT*2+UP*0.5, width=1.0)
        bar_red.set_color(RED)
        label_2x = etiqueta("2x", pos=LEFT*2+UP*1.5, color=INK, font_size=40)
        label_1x = etiqueta("1x", pos=RIGHT*2+UP*1.5, color=INK, font_size=40)
        callout_txt = callout("Estudio Chellappa et al., 2013", color=ORANGE, font_size=96).shift(UP*3.2)

        self.play(FadeIn(prota), FadeIn(bar_blue), FadeIn(bar_red), FadeIn(label_2x), FadeIn(label_1x), FadeIn(callout_txt))
        self.wait(4)