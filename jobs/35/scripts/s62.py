from manim import *
from zenn_rig import *

class S62(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.2+LEFT*3.5, 
            playera=PLAYERA_AZUL, 
            altura=2.6, 
            expresion='sorpresa', 
            pose='de_pie'
        )
        
        self.play(FadeIn(prota), run_time=0.8)
        
        mat = matraz(pos=RIGHT*3.5+DOWN*0.5, escala=1.2, liquido=TEAL)
        self.play(Create(mat), run_time=0.8)
        
        c = callout(
            "¡Reacción en cadena!", 
            color=ORANGE, 
            pos=RIGHT*3.0+UP*1.2
        )
        self.play(FadeIn(c), run_time=0.8)
        
        cambiar_cara(prota, 'euforico')
        self.wait(1.2)