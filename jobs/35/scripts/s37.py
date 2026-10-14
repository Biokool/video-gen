from manim import *
from zenn_rig import *

class S37(Scene):
    def construct(self):
        self.add(fondo(AZUL_MARINO))

        prota = protagonista(
            pos=DOWN*1.2+LEFT*3.5, 
            playera=PLAYERA_AZUL, 
            altura=2.4, 
            expresion='sorpresa', 
            pose='senalando'
        )
        
        ojo = ojo_grande(pos=RIGHT*3.2+UP*0.5, escala=1.2, iris=RED)
        
        c = callout(
            "¡Mentiras sobre tu mano!", 
            color=ORANGE, 
            pos=RIGHT*3.2+DOWN*1.5
        )

        self.play(
            FadeIn(prota),
            FadeIn(ojo),
            FadeIn(c),
            run_time=1.0
        )
        
        cambiar_cara(prota, 'miedo')
        
        self.wait(1.5)