from manim import *
from zenn_rig import *

class S040(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.0, playera="roja", altura=2.6, expresion="sorpresa", pose="de_pie")
        shield = caja(etiqueta="Escudo", pos=LEFT*3, width=1.5)
        droplet = matraz(escala=1.0, liquido=TEAL, pos=RIGHT*3)
        self.play(FadeIn(prota), FadeIn(shield), FadeIn(droplet), run_time=2)
        self.wait(2)
        self.play(prota.animate.shift(UP*0.3), run_time=1)
        self.wait(1)