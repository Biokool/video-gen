from manim import *
from zenn_rig import *

class S111(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_ROJA, altura=2.6, expresion='miedo', pose='brazos_cruzados')
        
        self.play(FadeIn(prota), run_time=0.8)
        
        c = callout("¡Batalla interna!", color=RED, pos=RIGHT*3.2+UP*0.5)
        self.play(Create(c), run_time=0.8)
        
        cambiar_cara(prota, 'sorpresa')
        
        self.wait(1.0)