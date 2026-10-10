from manim import *
from zenn_rig import *

class S59(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = version_prota(1, pos=DOWN*1.2+LEFT*3.5, altura=2.6)
        self.play(
            FadeIn(banda_titulo("¡CURIOSIDAD CIENTÍFICA!", color=ORANGE)),
            FadeIn(prota)
        )
        
        p = pez(pos=RIGHT*3.5+DOWN*1.5, escala=1.2)
        self.play(FadeIn(p))
        
        self.wait(2)