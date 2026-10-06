from manim import *
from zenn_rig import *

class S052(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3 + DOWN*1.2, playera="rosa", altura=2.6, expresion="sorpresa", pose='de_pie')
        heart = personaje(pos=RIGHT*2 + UP*0.5, cuerpo=RED, altura=1.2, expresion_tipo='normal')
        brain = personaje(pos=RIGHT*2 + DOWN*0.5, cuerpo=TEAL, altura=1.2, expresion_tipo='normal')
        fuego_icon = fuego(pos=LEFT*2 + UP*0.5, escala=1.0)

        self.play(FadeIn(prota), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(heart), FadeIn(brain), run_time=0.8)
        self.wait(0.3)
        self.play(FadeIn(fuego_icon), run_time=0.8)
        self.wait(0.3)
        self.play(prota.animate.shift(UP*0.3), run_time=0.2)
        self.play(prota.animate.shift(DOWN*0.3), run_time=0.2)
        self.wait(0.5)
        self.play(heart.animate.scale(1.2), brain.animate.scale(1.2), run_time=0.4)
        self.wait(0.2)
        self.play(heart.animate.scale(1/1.2), brain.animate.scale(1/1.2), run_time=0.4)
        self.wait(0.5)
        self.wait(1.0)