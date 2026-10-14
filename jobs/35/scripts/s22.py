from manim import *
from zenn_rig import *

class S22(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.2+LEFT*3.5, 
            playera=PLAYERA_TEAL, 
            altura=2.5, 
            expresion='pensando', 
            pose='de_pie'
        )
        
        cerebro = planeta(pos=RIGHT*3.2+UP*0.5, radio=1.2, color=TEAL)
        lupa_obj = lupa(pos=RIGHT*2.2+DOWN*0.8, escala=1.1, color=INK)
        
        msg = callout(
            "Especialización\nde hemisferios", 
            color=ORANGE, 
            pos=RIGHT*3.2+UP*2.0
        )
        
        self.play(
            FadeIn(prota),
            Create(cerebro),
            Create(lupa_obj),
            FadeIn(msg),
            run_time=1.0
        )
        
        cambiar_cara(prota, 'feliz')
        self.play(
            prota.animate.shift(UP*0.2),
            run_time=1.5
        )
        
        self.wait(1.5)