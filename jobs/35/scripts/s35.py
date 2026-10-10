from manim import *
from zenn_rig import *

class S35(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*3.5,
            playera=PLAYERA_AZUL,
            altura=2.5,
            expresion="mente_explotada",
            pose="senalando"
        )
        
        self.play(FadeIn(prota), run_time=0.8)
        
        c = cerebro = matraz(pos=UP*0.5 + RIGHT*2.5, escala=1.2, liquido=CORAL)
        self.play(Create(c), run_time=1.0)
        
        box = callout("¡Idea brillante!", color=ORANGE, pos=RIGHT*3.2 + UP*1.8)
        self.play(FadeIn(box), run_time=0.8)
        
        self.wait(1.4)