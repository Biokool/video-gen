from manim import *
from zenn_rig import *

class S102(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_TEAL,
            altura=2.6,
            expresion='alegria_pura',
            pose='senalando'
        )
        
        banda = banda_titulo("¡GRACIAS POR ACOMPAÑARNOS!", color=TEAL)
        
        reloj = reloj_pared(radius=1.2, pos=RIGHT*3.5 + DOWN*1.5, hora_3=True)
        
        self.play(
            FadeIn(banda),
            FadeIn(prota),
            FadeIn(reloj),
            run_time=1.0
        )
        
        cambiar_cara(prota, 'feliz')
        
        self.wait(9.7)