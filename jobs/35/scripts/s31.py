from manim import *
from zenn_rig import *

class S31(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        self.play(FadeIn(banda_titulo("¿Qué empuja la dominancia?", color=TEAL)))
        
        prota = protagonista(
            pos=DOWN*1.2+LEFT*3.5, 
            playera=PLAYERA_VERDE, 
            altura=2.6, 
            expresion="pensando", 
            pose="senalando"
        )
        self.play(FadeIn(prota))
        
        cerebro = digitos(pos=RIGHT*3.0+UP*0.5, size=1.8)
        self.play(Create(cerebro))
        
        c = etiqueta("¿Hemisferio dominante?", pos=RIGHT*3.2+UP*1.8, color=ORANGE, font_size=40)
        self.play(FadeIn(c))
        
        self.wait(5)