from manim import *
from zenn_rig import *

class S60(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        self.play(
            FadeIn(banda_titulo("¡Misterio resuelto!", color=ORANGE)),
            FadeIn(protagonista(pos=DOWN*1.3+LEFT*3.5, playera=PLAYERA_NARANJA, altura=2.4, expresion="alegria_pura", pose="senalando"))
        )
        
        c = caja("Datos", pos=RIGHT*3.2+UP*0.2, width=2.0)
        m = matraz(pos=RIGHT*3.2+DOWN*1.2, escala=0.9, liquido=TEAL)
        
        self.play(Create(c), FadeIn(m))
        self.play(FadeIn(etiqueta("¡Eureka!", pos=RIGHT*3.2+UP*1.9, color=RED, font_size=50, ancho_max=4.0)))
        self.wait(1.5)