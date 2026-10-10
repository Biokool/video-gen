from manim import *
from zenn_rig import *

class S36(Scene):
    def construct(self):
        self.add(fondo(AZUL_MARINO))
        
        self.play(
            FadeIn(version_prota(1, pos=DOWN*1.2+LEFT*3.5)),
            FadeIn(planeta(pos=RIGHT*3.5+UP*0.5, radio=1.2, color=TEAL))
        )
        
        self.play(
            FadeIn(callout("¡Exploración espacial!", color=ORANGE, pos=RIGHT*3.4+UP*1.5))
        )
        
        self.wait(2.5)