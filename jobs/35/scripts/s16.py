from manim import *
from zenn_rig import *

class S16(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        titulo = banda_titulo("LA GENÉTICA ES SOLO UNA PARTE", color=AZUL_MARINO)
        self.play(FadeIn(titulo))
        
        prota = protagonista(
            pos=DOWN*1.2+LEFT*3.5, 
            playera=PLAYERA_AZUL, 
            altura=2.6, 
            expresion="sorpresa", 
            pose="senalando"
        )
        self.play(FadeIn(prota))
        
        dna = adn(pos=RIGHT*3.0+UP*0.3, escala=1.2, color=TEAL)
        self.play(FadeIn(dna))
        
        lbl = etiqueta("¡Historia completa!", pos=RIGHT*3.2+DOWN*1.5, color=ORANGE, font_size=40)
        self.play(FadeIn(lbl))
        
        self.wait(3.0)