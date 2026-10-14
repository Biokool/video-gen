from manim import *
from zenn_rig import *

class S31(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        titulo = banda_titulo("EVOLUCIÓN Y ASIMETRÍA", color=TEAL)
        self.play(
            FadeIn(titulo),
            run_time=0.8
        )
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*4.0,
            playera=PLAYERA_VERDE,
            altura=2.5,
            expresion="pensando",
            pose="senalando"
        )
        
        d = dino(pos=DOWN*1.3 + RIGHT*3.5, color=TEAL, escala=0.9)
        cerebro = adn(pos=UP*0.5 + RIGHT*3.5, escala=0.8, color=CORAL)
        
        self.play(
            FadeIn(prota),
            FadeIn(d),
            FadeIn(cerebro),
            run_time=1.2
        )
        
        cambiar_cara(prota, "alegria_pura")
        
        self.wait(7.7)