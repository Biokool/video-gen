from manim import *
from zenn_rig import *

class S054(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3 + DOWN*1.2, playera="rosa", altura=2.5, expresion='feliz', pose='de_pie')
        tierra = planeta(pos=RIGHT*3 + DOWN*0.5, radio=0.95, color=TEAL)
        n1 = etiqueta("♪", pos=RIGHT*3 + UP*1, color=INK, font_size=40)
        n2 = etiqueta("♪", pos=RIGHT*2 + UP*1.5, color=INK, font_size=40)
        n3 = etiqueta("♪", pos=RIGHT*4 + UP*0.5, color=INK, font_size=40)
        notas = VGroup(n1, n2, n3)

        self.play(FadeIn(prota), FadeIn(tierra), FadeIn(notas), run_time=2)
        self.wait(2)