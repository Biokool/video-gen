from manim import *
from zenn_rig import *

class S014(Scene):
    def construct(self):
        prota = protagonista(
            pos=DOWN*1.2+LEFT*3.5,
            playera=PLAYERA_AZUL,
            altura=2.6,
            expresion='sorpresa',
            pose='de_pie'
        )
        frasco = matraz(pos=RIGHT*2.5+DOWN*0.5, escala=1.0, liquido=INK)
        dato = callout("<500 ml", color=ORANGE, pos=RIGHT*3.4+UP*1)
        etiqueta_texto = etiqueta("<500ml", pos=RIGHT*2.5+DOWN*0.5,
                                  color=INK, font_size=40, ancho_max=5.5)

        self.play(FadeIn(prota), run_time=1)
        self.play(FadeIn(frasco), run_time=1)
        self.play(FadeIn(dato), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(red_accent(frasco)), run_time=0.5)
        self.wait(1.5)
        self.play(FadeIn(etiqueta_texto), run_time=1)
        self.wait(2.5)