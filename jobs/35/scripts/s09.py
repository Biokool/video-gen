from manim import *
from zenn_rig import *

class S09(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.3+LEFT*4.0, 
            playera=PLAYERA_VERDE, 
            altura=2.5, 
            expresion='pensando', 
            pose='senalando'
        )
        
        titulo = banda_titulo("¿Influencia materna y hormonas en la lateralidad?", color=TEAL)
        
        adn_obj = adn(pos=RIGHT*3.5+DOWN*1.5, escala=0.8, color=TEAL)
        
        self.play(
            FadeIn(prota),
            FadeIn(titulo),
            Create(adn_obj),
            run_time=1.5
        )
        
        cambiar_cara(prota, 'sorpresa')
        
        self.wait(6.5)