from manim import *
from zenn_rig import *

class S105(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN * 1.2 + LEFT * 3.0,
            playera=PLAYERA_TEAL,
            altura=2.6,
            expresion='euforico',
            pose='de_pie'
        )
        
        msj = callout("¡Hasta Pronto!", color=ORANGE, pos=RIGHT * 3.2 + DOWN * 1.0)
        
        self.play(
            FadeIn(prota, shift=UP),
            FadeIn(msj, shift=DOWN),
            run_time=1.5
        )
        
        cambiar_cara(prota, 'feliz')
        self.wait(0.5)
        
        self.wait(2.0)
        
        self.play(
            FadeOut(prota),
            FadeOut(msj),
            run_time=1.0
        )