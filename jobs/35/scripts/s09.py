from manim import *
from zenn_rig import *

class S09(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_AZUL, altura=2.6, expresion='sorpresa', pose='senalando')
        self.add(prota)
        
        et = etiqueta("¿Zurdo?", pos=RIGHT*3.0+UP*1.5, color=INK)
        self.add(et)
        
        c = lapida(texto='10%', pos=RIGHT*3.0+DOWN*0.5, ancho=2.0)
        self.add(c)
        
        self.play(FadeIn(c), run_time=1.0)
        self.wait(5.0)
        self.play(FadeOut(prota), FadeOut(c), FadeOut(et), run_time=1.0)