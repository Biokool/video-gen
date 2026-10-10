from manim import *
from zenn_rig import *

class S46(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        self.play(
            FadeIn(
                banda_titulo("¡Hora de programar con estilo!", color=ORANGE)
            )
        )
        
        prota = version_prota(1, pos=DOWN*1.3+LEFT*3.2)
        self.play(FadeIn(prota))
        
        c = reloj_pared(radius=1.2, pos=RIGHT*3.0+UP*0.5, hora_3=True)
        self.play(Create(c))
        
        texto_dato = etiqueta("¡Rápido y eficiente!", pos=RIGHT*3.2+DOWN*1.2, color=AZUL_MARINO)
        self.play(FadeIn(texto_dato))
        
        self.wait(2.0)