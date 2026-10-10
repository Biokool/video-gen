from manim import *
from zenn_rig import *

class S38(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        self.play(
            FadeIn(banda_titulo("¡MUNDO SECRETO!", color=CORAL)),
            FadeIn(protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_AZUL, altura=2.6, expresion="sorpresa", pose="de_pie"))
        )
        
        p_derecho = perro(pos=RIGHT*3.5+DOWN*1.2, color='#C98A4B', escala=1.2)
        self.play(FadeIn(p_derecho, shift=UP))
        
        self.play(
            FadeIn(etiqueta("¡Sorpresa canina!", pos=RIGHT*3.2+UP*1.0, color=ORANGE, font_size=40, ancho_max=5.5))
        )
        
        self.wait(1.5)