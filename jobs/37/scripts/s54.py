from manim import *
from zenn_rig import *

class S54(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        banda = banda_titulo("¿POR QUÉ SIGUES?", color=ORANGE)
        self.play(FadeIn(banda, shift=DOWN))
        
        prota = version_prota(4, pos=DOWN*1.8 + LEFT*3.0)
        prota.set_height(2.4)
        self.play(FadeIn(prota, shift=UP))
        
        matraz_prop = matraz(pos=RIGHT*3.8 + DOWN*0.5, escala=0.8, liquido=TEAL)
        self.play(FadeIn(matraz_prop, scale=0.8))
        
        self.wait(0.5)
        
        cambiar_cara(prota, "pensando")
        self.wait(1.5)
        
        self.play(
            FadeOut(banda),
            FadeOut(prota),
            FadeOut(matraz_prop),
        )
        
        self.play(
            FadeOut(*self.mobjects),
            run_time=0.5
        )
        
        self.wait(0.5)