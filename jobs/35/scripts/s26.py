from manim import *
from zenn_rig import *

class S26(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera=PLAYERA_AZUL, 
            altura=2.6, 
            expresion="euforico", 
            pose="senalando"
        )
        
        cerebro_corva = adn(pos=RIGHT*3.0 + UP*1.0, escala=1.2, color=TEAL)
        guante = red_accent(cerebro_corva, scale=1.1)
        
        msj = callout("¡Hemisferio derecho!", color=ORANGE, pos=RIGHT*3.0 + DOWN*1.5)
        
        self.play(FadeIn(prota), Create(cerebro_corva), Create(guante))
        self.play(Write(msj))
        self.wait(3.0)