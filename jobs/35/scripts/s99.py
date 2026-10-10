from manim import *
from zenn_rig import *

class S99(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        titulo = banda_titulo("¡La lateralidad nace en el movimiento!", color=ORANGE)
        self.play(FadeIn(titulo))
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.8,
            playera=PLAYERA_NARANJA,
            altura=2.4,
            expresion="mente_explotada",
            pose="senalando"
        )
        self.play(FadeIn(prota))
        
        bebe = adn(pos=RIGHT*3.5 + UP*0.5, escala=1.2)
        self.play(Create(bebe))
        
        dato = etiqueta("¡Primeras patadas en el útero!", pos=RIGHT*3.2 + DOWN*1.0, color=TEAL)
        self.play(FadeIn(dato))
        
        self.wait(2.0)
        
        self.play(
            FadeOut(prota),
            FadeOut(bebe),
            FadeOut(dato),
            FadeOut(titulo)
        )
        self.wait(1.0)