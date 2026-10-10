from manim import *
from zenn_rig import *

class S39(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        self.play(FadeIn(banda_titulo("¡CURIOSIDAD CIENTÍFICA!", color=ORANGE)))
        
        prota = protagonista(pos=DOWN*1.5 + LEFT*3.5, playera=PLAYERA_NARANJA, altura=2.4, expresion='sorpresa', pose='senalando')
        self.play(FadeIn(prota))
        
        c = caja(etiqueta="DATOS", pos=RIGHT*3.5 + UP*0.5, width=2.0)
        m = matraz(pos=RIGHT*3.5 + DOWN*1.0, escala=1.2, liquido=TEAL)
        self.play(Create(c), FadeIn(m))
        
        et = etiqueta("¡Descubrimiento!", pos=RIGHT*3.5 + UP*2.2, color=ORANGE, font_size=50)
        self.play(FadeIn(et))
        
        self.wait(2.0)