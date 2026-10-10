from manim import *
from zenn_rig import *

class S15(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_AZUL, altura=2.6, expresion='pensando', pose='senalando')
        
        balanza = grafica_barras(pos=RIGHT*3.0+UP*0.5, valores=(3, 5, 4, 6), ancho=3.5, color=TEAL, etiquetas=None)
        etq_gen = etiqueta("genes", pos=RIGHT*3.0+UP*2.0, color=INK, font_size=40)
        
        c = callout("¡Inclinan la balanza!", color=ORANGE, pos=RIGHT*3.0+DOWN*1.5)
        
        self.play(FadeIn(prota), Create(balanza), FadeIn(etq_gen))
        self.play(FadeIn(c))
        self.wait(4.0)