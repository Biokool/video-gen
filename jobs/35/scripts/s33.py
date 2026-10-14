from manim import *
from zenn_rig import *

class S33(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*3.8, 
            playera=PLAYERA_VERDE, 
            altura=2.6, 
            expresion='alegria_pura', 
            pose='senalando'
        )
        
        martillo_prop = casco_vikingo(pos=RIGHT*2.5 + UP*1.0, escala=1.2)
        nota_prop = vela(pos=RIGHT*2.5 + DOWN*1.2, escala=1.1)
        
        c = callout(
            "¡Herramientas y comunicación!", 
            color=AZUL_MARINO, 
            pos=RIGHT*3.2 + UP*0.2
        )
        
        flecha = arrow(RIGHT*1.2, RIGHT*2.1, color=INK, width=6)
        
        self.play(
            FadeIn(prota),
            Create(martillo_prop),
            Create(nota_prop),
            run_time=1.0
        )
        
        self.play(
            FadeIn(c),
            Create(flecha),
            run_time=1.0
        )
        
        self.wait(5.0)