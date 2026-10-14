from manim import *
from zenn_rig import *

class S15(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera=PLAYERA_VERDE, 
            altura=2.6, 
            expresion='mente_explotada', 
            pose='senalando'
        )
        
        cerebro = adn(pos=RIGHT*3.0 + UP*0.5, escala=1.2, color=TEAL)
        
        titulo = banda_titulo("Control Motor y Lenguaje", color=INK)
        
        self.play(
            FadeIn(titulo),
            FadeIn(prota),
            FadeIn(cerebro),
            run_time=1.5
        )
        
        cambiar_cara(prota, 'alegria_pura')
        
        self.wait(4.5)