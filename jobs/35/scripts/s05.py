from manim import *
from zenn_rig import *

class S05(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_NARANJA, altura=2.4, expresion='confundido', pose='de_pie')
        
        self.play(FadeIn(prota), run_time=0.8)
        
        c_callout = callout("¿Por qué hay zurdos y diestros?", color=ORANGE, pos=RIGHT*3.2+UP*1.0)
        self.play(Create(c_callout), run_time=1.0)
        
        cambiar_cara(prota, 'sorpresa')
        self.play(prota.animate.shift(UP*0.2), run_time=0.5)
        
        self.wait(1.7)