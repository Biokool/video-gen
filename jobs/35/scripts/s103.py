from manim import *
from zenn_rig import *

class S103(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=50, color=WHITE))
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera=PLAYERA_TEAL, 
            altura=2.6, 
            expresion='alegria_pura', 
            pose='de_pie'
        )
        
        c = callout(
            "¡Cada uno es un universo!", 
            color=ORANGE, 
            pos=RIGHT*3.2 + UP*0.8
        )
        
        planeta_viz = planeta(pos=RIGHT*3.5 + DOWN*1.5, radio=1.2, color=TEAL)
        
        self.play(FadeIn(prota), FadeIn(planeta_viz), FadeIn(c), run_time=1.5)
        cambiar_cara(prota, 'feliz')
        self.wait(5.5)
        self.play(FadeOut(prota), FadeOut(c), FadeOut(planeta_viz), run_time=1.0)