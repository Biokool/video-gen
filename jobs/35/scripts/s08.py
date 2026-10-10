from manim import *
from zenn_rig import *

class S08(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.2+LEFT*3.5, 
            playera=PLAYERA_AZUL, 
            altura=2.6, 
            expresion='alegria_pura', 
            pose='senalando'
        )
        
        lap = lapida(texto='LÁPIZ', pos=RIGHT*2.5+UP*0.5)
        
        av = arrow(start=LEFT*2.0+UP*0.5, end=RIGHT*1.2+UP*0.5, color=INK)
        
        c = callout("¡Boom! Eres diestro.", color=ORANGE, pos=RIGHT*3.0+UP*1.8)
        
        self.play(
            FadeIn(prota),
            Create(lap),
            run_time=1.0
        )
        self.play(
            Create(av),
            FadeIn(c),
            run_time=1.5
        )
        self.wait(5.5)