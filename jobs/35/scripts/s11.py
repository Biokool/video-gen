from manim import *
from zenn_rig import *

class S11(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.2+LEFT*3.5, 
            playera=PLAYERA_AMARILLA, 
            altura=2.5, 
            expresion="pensando", 
            pose="senalando"
        )
        
        c = callout(
            "¿Genética + Ambiente = ¿Zurdo?", 
            color=CORAL, 
            pos=RIGHT*3.4+UP*0.8
        )
        
        arr = arrow(LEFT*2.0 + UP*0.5, RIGHT*1.5 + UP*0.5, color=INK, width=8)
        cerebro_prop = adn(pos=RIGHT*3.4+DOWN*1.2, escala=0.9, color=TEAL)
        
        self.play(FadeIn(prota), FadeIn(c), Create(arr), FadeIn(cerebro_prop), run_time=1.5)
        cambiar_cara(prota, "sorpresa")
        self.wait(7.5)