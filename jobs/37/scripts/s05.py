from manim import *
from zenn_rig import *

class S05(Scene):
    def construct(self):
        self.add(fondo(AZUL_MARINO))
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="confundido",
            pose="brazos_cruzados"
        )
        
        casco = casco_vikingo(pos=RIGHT*3.5 + UP*0.5, escala=1.4)
        
        c = callout("Fantasma histórico", color=ORANGE, pos=RIGHT*3.5 + DOWN*1.5)
        
        self.play(
            FadeIn(prota, shift=UP*0.5),
            FadeIn(casco, shift=DOWN*0.5),
            run_time=1.0
        )
        
        self.play(
            FadeIn(c, shift=UP*0.2),
            run_time=0.8
        )
        
        cambiar_cara(prota, "sorpresa")
        self.wait(0.5)
        
        self.wait(1.7)