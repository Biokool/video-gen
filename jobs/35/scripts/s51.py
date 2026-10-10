from manim import *
from zenn_rig import *

class S51(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="mente_explotada",
            pose="senalando"
        )
        
        self.play(FadeIn(prota))
        
        t_sec = reloj_pared(radius=1.2, pos=UP*0.5 + RIGHT*3.0, hora_3=True)
        self.play(Create(t_sec))
        
        c = callout("¡El tiempo vuela!", color=ORANGE, pos=RIGHT*3.0 + DOWN*1.5)
        self.play(FadeIn(c))
        
        self.wait(2.0)