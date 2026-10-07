from manim import *
from zenn_rig import *

class S038(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3.5+DOWN*1.2, playera="roja", altura=2.6, expresion="enojado", pose="de_pie")
        tv = caja(etiqueta="TV", pos=RIGHT*3.5, width=1.8)
        signal = curva(pos=RIGHT*3.5+UP*2.0, ancho=2.5, alto=0.6, color=INK, acento=RED)
        film = pagina_calendario(width=1.7)
        film.shift(RIGHT*3.5+DOWN*2.0)
        right_group = VGroup(tv, signal, film)
        etiqueta_texto = etiqueta("Señal entrecortada", pos=RIGHT*5.0, color=INK, font_size=40, ancho_max=5.5)
        self.play(FadeIn(prota), run_time=1)
        self.play(FadeIn(right_group), run_time=1.5)
        self.play(FadeIn(etiqueta_texto), run_time=1)
        self.wait(0.5)