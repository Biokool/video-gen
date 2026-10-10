from manim import *
from zenn_rig import *

class S95(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_AZUL, altura=2.6, expresion="pensando", pose="de_pie")
        
        self.play(FadeIn(prota), run_time=0.5)
        
        c = calendario(pos=RIGHT*3.0+UP*0.5, width=2.2)
        self.play(Create(c), run_time=1.0)
        
        txt = callout("¿Zurdo o diestro?", color=ORANGE, pos=RIGHT*3.0+DOWN*1.8)
        self.play(FadeIn(txt), run_time=1.0)
        
        cambiar_cara(prota, "sorpresa")
        self.wait(2.0)
        
        self.play(FadeOut(prota), FadeOut(c), FadeOut(txt), run_time=1.0)