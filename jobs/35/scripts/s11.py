from manim import *
from zenn_rig import *

class S11(Scene):
    def construct(self):
        self.add(fondo(AZUL_MARINO))
        
        prota = protagonista(
            pos=DOWN*1.5 + LEFT*3.5,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="pensando",
            pose="de_pie"
        )
        
        m = matraz(pos=RIGHT*2.5 + DOWN*0.2, escala=1.4, liquido=TEAL)
        a = adn(pos=RIGHT*2.5 + UP*1.8, escala=0.8, color=TEAL)
        
        self.play(
            FadeIn(prota),
            FadeIn(m),
            FadeIn(a),
            run_time=1.0
        )
        
        cambiar_cara(prota, "sorpresa")
        self.wait(0.5)
        
        self.wait(1.5)