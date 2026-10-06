from manim import *
from zenn_rig import *

class S024(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3.5 + DOWN*1.2, playera="verde", altura=2.6, expresion="sorpresa", pose="de_pie")
        curva_obj = curva(pos=RIGHT*2 + UP*0.5, ancho=5.2, alto=2.8, color=INK, acento=RED)
        moneda = moneda_dorada(texto='$', pos=LEFT*5 + DOWN*1, radio=0.8)
        txt = callout("Latidos más rápidos", color=ORANGE)

        self.play(FadeIn(prota), FadeIn(curva_obj), FadeIn(moneda), Write(txt), run_time=0.8)
        self.wait(0.5)

        self.play(moneda.animate.shift(RIGHT*6), run_time=2)
        self.play(curva_obj.animate.scale(1.2), run_time=0.4)
        self.play(curva_obj.animate.scale(1/1.2), run_time=0.4)
        self.play(moneda.animate.shift(LEFT*6), run_time=2)
        self.play(curva_obj.animate.scale(1.2), run_time=0.4)
        self.play(curva_obj.animate.scale(1/1.2), run_time=0.4)

        self.wait(2)