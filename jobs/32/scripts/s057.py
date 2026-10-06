from manim import *
from zenn_rig import *

class S057(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera='teal', altura=2.6, expresion='feliz', pose='de_pie')
        button = caja(etiqueta='SUSCRÍBETE', pos=DOWN*1.2+RIGHT*3.5, width=2.0)
        bell = moneda_dorada(texto='🔔', pos=UP*2+LEFT*4, radio=0.8)

        self.play(FadeIn(prota), run_time=1)
        self.play(FadeIn(button), run_time=1)
        self.play(FadeIn(bell), run_time=1)
        self.wait(3)  # tiempo equivalente al cambio de expresión y espera original
        self.play(FadeOut(prota), FadeOut(button), FadeOut(bell), run_time=1)