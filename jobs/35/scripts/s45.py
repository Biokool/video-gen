from manim import *
from zenn_rig import *

class S45(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN * 1.3 + LEFT * 3.5,
            playera=PLAYERA_TEAL,
            altura=2.5,
            expresion="sorpresa",
            pose="senalando"
        )
        
        l = lupa(pos=RIGHT * 2.0 + UP * 0.5, escala=1.4)
        c = callout("Fetos ya muestran preferencia manual", color=TEAL, pos=RIGHT * 3.4 + UP * 1.5)
        
        self.play(
            FadeIn(prota),
            FadeIn(l),
            FadeIn(c),
            run_time=1.5
        )
        
        cambiar_cara(prota, "feliz")
        
        self.wait(7.0)