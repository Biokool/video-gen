from manim import *
from zenn_rig import *

class S08(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        titulo = banda_titulo("ENTORNO PRENATAL", color=TEAL)
        self.play(FadeIn(titulo))
        
        prota = protagonista(pos=DOWN*1.2+LEFT*3.8, playera=PLAYERA_VERDE, altura=2.4, expresion='pensando', pose='senalando')
        self.play(FadeIn(prota))
        
        dna = adn(pos=RIGHT*2.5+UP*0.5, escala=1.0, color=TEAL)
        mat = matraz(pos=RIGHT*2.5+DOWN*1.5, escala=1.0, liquido=TEAL)
        
        flecha1 = arrow(LEFT*1.5+UP*0.5, RIGHT*1.2+UP*0.5, color=INK, width=8)
        flecha2 = arrow(LEFT*1.5+DOWN*0.5, RIGHT*1.2+DOWN*0.5, color=INK, width=8)
        
        self.play(
            FadeIn(dna),
            FadeIn(mat),
            FadeIn(flecha1),
            FadeIn(flecha2),
            run_time=1.5
        )
        
        cambiar_cara(prota, 'sorpresa')
        self.wait(4.0)