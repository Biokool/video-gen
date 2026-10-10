from manim import *
from zenn_rig import *

class S56(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*3.8,
            playera=PLAYERA_AZUL,
            altura=2.5,
            expresion="mente_explotada",
            pose="senalando"
        )
        
        self.play(FadeIn(prota))
        
        t = banda_titulo("¡EL UNIVERSO ES INFINITO!", color=ORANGE)
        self.play(Write(t))
        
        planeta_obj = planeta(pos=RIGHT*3.2 + UP*0.5, radio=1.3, color=TEAL)
        self.play(Create(planeta_obj))
        
        lbl = etiqueta("¡Espacio sin fin!", pos=RIGHT*3.2 + DOWN*1.5, color=INK)
        self.play(FadeIn(lbl))
        
        self.wait(2.0)