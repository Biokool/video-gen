from manim import *
from zenn_rig import *

class S18(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        self.add(banda_titulo("LA LATERALIDAD ES UN ESPECTRO", color=ORANGE))
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*3.8, 
            playera=PLAYERA_AMARILLA, 
            altura=2.4, 
            expresion='confundido', 
            pose='de_pie'
        )
        self.add(prota)
        
        c = curva(pos=RIGHT*2.5 + UP*0.2, ancho=5.0, alto=2.2, color=INK, acento=TEAL)
        self.add(c)
        
        etic = etiqueta("Espectro continuo", pos=RIGHT*2.5 + DOWN*1.5)
        self.add(etic)
        
        self.play(
            FadeIn(c, shift=UP*0.3),
            run_time=1.0
        )
        self.play(
            FadeIn(etic, shift=UP*0.2),
            run_time=1.0
        )
        
        cambiar_cara(prota, 'pensando')
        
        self.wait(3.5)