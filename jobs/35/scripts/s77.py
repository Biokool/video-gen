from manim import *
from zenn_rig import *

class S77(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*3.2,
            playera=PLAYERA_ROJA,
            altura=2.5,
            expresion="pensando",
            pose="de_pie"
        )
        
        self.play(FadeIn(prota), run_time=1)
        
        c = callout(
            text="Tu conciencia se adapta",
            color=ORANGE,
            pos=RIGHT*2.8 + UP*0.8
        )
        
        self.play(FadeIn(c, shift=LEFT), run_time=1)
        
        cambiar_cara(prota, "sorpresa")
        
        self.wait(1.5)