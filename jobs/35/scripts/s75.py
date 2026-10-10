from manim import *
from zenn_rig import *

class S75(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(pos=DOWN*1.5+LEFT*3.5, playera=PLAYERA_AZUL, altura=2.4, expresion='pensando', pose='de_pie')
        
        self.play(FadeIn(prota))
        
        c = curva(pos=RIGHT*2.5+UP*0.5, ancho=4.5, alto=2.8)
        et = etiqueta("¿Zurdo o diestro?", (2.5, -1.8))
        
        self.play(Create(c), FadeIn(et))
        cambiar_cara(prota, 'sorpresa')
        
        co = callout("Predisposición natural vs. Aprendizaje", color=ORANGE, pos=RIGHT*3.0+UP*2.0)
        self.play(FadeIn(co))
        
        self.wait(2.5)