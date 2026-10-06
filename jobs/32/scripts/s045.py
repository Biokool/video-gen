from manim import *
from zenn_rig import *

class S045(Scene):
    def construct(self):
        prota = protagonista(pos=ORIGIN, playera="amarilla", altura=3.0, expresion="sorpresa", pose="de_pie")
        muscle = curva(pos=LEFT*3 + DOWN*0.5, ancho=2.0, alto=1.0, color=INK, acento=RED)
        organ = planeta(pos=RIGHT*3 + DOWN*0.5, radio=0.95, color=TEAL)
        label_muscle = etiqueta("Fibra débil", pos=LEFT*3 + UP*0.5, color=INK, font_size=40, ancho_max=5.5)
        label_organ = etiqueta("Órgano lento", pos=RIGHT*3 + UP*0.5, color=INK, font_size=40, ancho_max=5.5)

        self.play(FadeIn(prota), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(muscle), FadeIn(organ), run_time=1)
        self.play(FadeIn(label_muscle), FadeIn(label_organ), run_time=0.5)
        self.wait(1)
        self.play(muscle.animate.scale(1.2), run_time=0.5)
        self.play(muscle.animate.scale(1/1.2), run_time=0.5)
        self.wait(1)