from manim import *
from zenn_rig import *

class S35(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.2+LEFT*3.5, 
            playera=PLAYERA_ROSA, 
            altura=2.5, 
            expresion='pensando', 
            pose='de_pie'
        )
        
        l = lupa(pos=RIGHT*2.5+UP*0.2, escala=1.2, color=INK)
        c = camino(width=5.0, pos=RIGHT*2.5+DOWN*1.2)
        
        self.play(
            FadeIn(prota),
            FadeIn(l),
            FadeIn(c),
            run_time=1.0
        )
        
        co = callout(
            "¿Algo más por descubrir?", 
            color=ORANGE, 
            pos=RIGHT*3.0+UP*1.8
        )
        
        cambiar_cara(prota, 'sorpresa')
        
        self.play(
            FadeIn(co),
            run_time=1.0
        )
        
        self.wait(2.0)