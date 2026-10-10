from manim import *
from zenn_rig import *

class S53(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera=PLAYERA_NARANJA, 
            altura=2.6, 
            expresion='mente_explotada', 
            pose='de_pie'
        )
        
        self.play(FadeIn(prota, shift=UP))
        
        c = callout("¡La energía no se crea ni se destruye!", color=ORANGE, pos=RIGHT*3.0 + UP*1.0)
        self.play(Write(c))
        
        mat = matraz(pos=RIGHT*3.0 + DOWN*1.0, escala=1.2, liquido=TEAL)
        self.play(Create(mat))
        
        self.wait(2)