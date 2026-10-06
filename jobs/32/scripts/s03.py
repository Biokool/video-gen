from manim import *
from zenn_rig import *

class S03(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3.5 + DOWN*1.2, playera='naranja', altura=2.5, expresion='enojado', pose='senalando')
        vaso = caja(etiqueta='vaso', pos=RIGHT*3 + DOWN*0.5, width=1.0)
        flecha = arrow(start=prota.get_center() + RIGHT*0.5, end=vaso.get_center() + LEFT*0.5, color=INK, width=8)
        self.play(FadeIn(prota), FadeIn(vaso))
        self.play(Create(flecha))
        self.wait(1.5)