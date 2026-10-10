from manim import *
from zenn_rig import *

class S61(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera=PLAYERA_AZUL, 
            altura=2.6, 
            expresion='sorpresa', 
            pose='senalando'
        )
        
        mat = matraz(pos=RIGHT*3.0 + DOWN*0.5, escala=1.2, liquido=TEAL)
        
        self.play(
            FadeIn(prota),
            Create(mat),
            run_time=1.0
        )
        
        c = callout("¡Eureka!", color=ORANGE, pos=RIGHT*3.2 + UP*1.5)
        self.play(FadeIn(c), run_time=0.8)
        
        self.wait(1.5)