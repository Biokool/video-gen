from manim import *
from zenn_rig import *

class S63(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*3.5, 
            playera=PLAYERA_AZUL, 
            altura=2.4, 
            expresion='pensando', 
            pose='de_pie'
        )
        
        m = matraz(pos=RIGHT*2.5 + DOWN*0.2, escala=1.2, liquido=ORANGE)
        ojo = ojo_grande(pos=RIGHT*2.5 + UP*1.8, escala=0.8, iris=TEAL)
        
        self.play(
            FadeIn(prota),
            Create(m),
            FadeIn(ojo),
            run_time=1.5
        )
        
        cambiar_cara(prota, 'mente_explotada')
        self.wait(1.0)
        
        c = callout("Hormonas fetales", color=ORANGE, pos=RIGHT*3.2+DOWN*1.2)
        self.play(FadeIn(c), run_time=1.0)
        
        self.wait(8.0)
        
        self.play(
            FadeOut(prota),
            FadeOut(m),
            FadeOut(ojo),
            FadeOut(c),
            run_time=1.5
        )