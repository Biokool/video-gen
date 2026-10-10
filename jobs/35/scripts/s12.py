from manim import *
from zenn_rig import *

class S12(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        self.play(FadeIn(banda_titulo("¿Cómo ocurre?", color=ORANGE)))
        
        prota = protagonista(
            pos=DOWN*1.2+LEFT*3.5, 
            playera=PLAYERA_AZUL, 
            altura=2.5, 
            expresion="confundido", 
            pose="senalando"
        )
        self.play(FadeIn(prota))
        
        adn_obj = adn(pos=RIGHT*3.0+UP*0.5, escala=1.2, color=TEAL)
        lupa_obj = lupa(pos=RIGHT*1.8+DOWN*1.0, escala=1.1, color=INK)
        
        self.play(Create(adn_obj), FadeIn(lupa_obj))
        
        lab = etiqueta("¿Gen del zurdo? Más complejo.", pos=RIGHT*3.3+UP*2.0, color=CORAL)
        self.play(FadeIn(lab))
        
        cambiar_cara(prota, "mente_explotada")
        self.wait(3.0)