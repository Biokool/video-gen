from manim import *
from zenn_rig import *

class S50(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = version_prota(1, pos=DOWN*1.2+LEFT*3.5)
        self.play(FadeIn(prota))
        
        caja_obs = caja("IDEAS", pos=RIGHT*3.0+UP*0.2, width=2.0)
        self.play(Create(caja_obs))
        
        cambiar_cara(prota, "sorpresa")
        
        dato = callout("¡Eureka!", color=ORANGE, pos=RIGHT*3.4+UP*2.0)
        self.play(FadeIn(dato))
        
        self.wait(2.0)