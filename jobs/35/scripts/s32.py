from manim import *
from zenn_rig import *

class S32(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.3+LEFT*3.5, 
            playera=PLAYERA_VERDE, 
            altura=2.6, 
            expresion='pensando', 
            pose='de_pie'
        )
        
        reloj = reloj_pared(radius=1.2, pos=RIGHT*3.0+UP*0.5, hora_3=True)
        
        txt = callout(
            "¿Gradual o de repente?", 
            color=ORANGE, 
            pos=RIGHT*3.0+DOWN*1.8
        )
        
        self.play(
            FadeIn(prota),
            FadeIn(reloj),
            FadeIn(txt),
            run_time=1.5
        )
        
        cambiar_cara(prota, 'sorpresa')
        
        self.wait(1.5)