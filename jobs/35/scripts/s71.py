from manim import *
from zenn_rig import *

class S71(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=30, color=WHITE))
        
        prota = version_prota(5, pos=DOWN*1.3+LEFT*3.5)
        cambiar_cara(prota, "sorpresa")
        
        call = callout("¿Algo más?", color=YELLOW, pos=RIGHT*3.2+UP*1.0)
        
        arr = arrow(LEFT*2.0 + UP*0.5, RIGHT*1.5 + UP*0.5, color=ORANGE, width=10)
        
        self.play(
            FadeIn(prota, shift=UP),
            FadeIn(call, shift=DOWN),
            Create(arr),
            run_time=1.5
        )
        
        self.play(
            cambiar_prota_expr(prota, "pensando") if hasattr(self, 'cambiar_prota_expr') else FadeIn(VGroup()),
            run_time=2.0
        )
        
        self.wait(0.5)