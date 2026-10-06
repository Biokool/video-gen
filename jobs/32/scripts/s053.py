from manim import *
from zenn_rig import *

class S053(Scene):
    def construct(self):
        prot = protagonista(pos=LEFT*4 + DOWN*1.2, playera="rosa", altura=2.6, expresion='mente_explotada', pose='de_pie')
        cerebro = personaje(pos=RIGHT*4 + UP*0.5, cuerpo=TEAL, altura=2.2, expresion_tipo='triste')
        celula = personaje(pos=RIGHT*2 + DOWN*1.5, cuerpo=CORAL, altura=2.0, expresion_tipo='preocupado')
        corazon = personaje(pos=LEFT*2 + DOWN*1.5, cuerpo=RED, altura=2.2, expresion_tipo='feliz')
        self.play(FadeIn(prot, cerebro, celula, corazon), run_time=2)
        self.wait(1)
        self.play(
            cerebro.animate.scale(0.8),
            celula.animate.shift(LEFT*0.5),
            corazon.animate.scale(1.3),
            run_time=1.5
        )
        self.wait(1)
        self.play(
            cerebro.animate.scale(1/0.8),
            celula.animate.shift(RIGHT*0.5),
            corazon.animate.scale(1/1.3),
            run_time=1.5
        )
        self.wait(1)
        self.play(prot.animate.shift(UP*0.3), run_time=1)
        self.wait(0.5)
        self.play(prot.animate.shift(DOWN*0.3), run_time=1)
        self.wait(1)