from manim import *
from zenn_rig import *

class S87(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        titulo = banda_titulo("TESTOSTERONA Y LATERALIDAD", color=ORANGE)
        self.play(FadeIn(titulo))
        
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_AZUL, altura=2.4, expresion='pensando', pose='de_pie')
        self.play(FadeIn(prota))
        
        dna = adn(pos=RIGHT*3.0+UP*0.5, escala=0.9, color=TEAL)
        self.play(FadeIn(dna))
        
        et = etiqueta("Impacto en desarrollo fetal", pos=RIGHT*3.2+DOWN*1.0, color=INK)
        self.play(FadeIn(et))
        
        self.wait(2.0)
        
        cambiar_cara(prota, 'sorpresa')
        self.play(prota.animate.shift(RIGHT*0.5))
        
        self.wait(2.0)