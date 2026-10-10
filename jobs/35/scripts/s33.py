from manim import *
from zenn_rig import *

class S33(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        self.play(
            FadeIn(banda_titulo("El útero es tu primera escuela", color=CORAL)),
            FadeIn(matraz(pos=LEFT*2.5 + DOWN*0.4, escala=1.2, liquido=RED))
        )
        
        prota = protagonista(pos=RIGHT*2.5 + DOWN*1.2, playera=PLAYERA_AZUL, altura=2.6, expresion="mente_explotada", pose="senalando")
        self.play(FadeIn(prota))
        
        self.play(
            FadeIn(etiqueta("¡Aprendizaje prenatal!", pos=LEFT*3.0 + UP*1.0, color=ORANGE, font_size=40))
        )
        
        self.wait(1.5)