from manim import *
from zenn_rig import *

class S34(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*3.8, 
            playera=PLAYERA_AZUL, 
            altura=2.4, 
            expresion="sorpresa", 
            pose="senalando"
        )
        
        self.play(FadeIn(prota), run_time=0.6)
        
        m = matraz(pos=RIGHT*2.5 + DOWN*0.2, escala=1.2, liquido=CORAL)
        f = fuego(pos=RIGHT*2.5 + DOWN*1.7, escala=0.9)
        
        self.play(Create(m), FadeIn(f), run_time=0.8)
        
        c = callout(text="¡Reacción exotérmica!", color=ORANGE, pos=RIGHT*3.2 + UP*1.2)
        self.play(Write(c), run_time=0.8)
        
        self.wait(1.8)