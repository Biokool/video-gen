from manim import *
from zenn_rig import *

class S45(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*3.5, 
            playera=PLAYERA_AZUL, 
            altura=2.5, 
            expresion='sorpresa', 
            pose='senalando'
        )
        
        reloj = reloj_pared(radius=1.2, pos=RIGHT*3.0 + UP*0.5, hora_3=True)
        
        c = callout(
            text="¡El tiempo vuela!", 
            color=ORANGE, 
            pos=RIGHT*3.2 + DOWN*1.5
        )
        
        self.play(
            FadeIn(prota),
            FadeIn(reloj),
            FadeIn(c),
            run_time=1.0
        )
        
        cambiar_cara(prota, 'alegria_pura')
        self.wait(2.5)