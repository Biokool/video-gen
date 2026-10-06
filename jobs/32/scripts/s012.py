from manim import *
from zenn_rig import *

class S012(Scene):
    def construct(self):
        banda = banda_titulo("Plan de emergencia", color=ORANGE)
        prota = protagonista(pos=DOWN*1.2 + LEFT*2.5, playera=PLAYERA_AZUL, altura=2.4, expresion="pensando", pose="de_pie")
        kidney = caja("Riñón", pos=DOWN*1.2, width=1.5)
        shield = caja("Escudo", pos=DOWN*1.2 + RIGHT*2.5, width=1.5)

        self.play(FadeIn(banda), run_time=1)
        self.play(FadeIn(prota), FadeIn(kidney), FadeIn(shield), run_time=1.5)
        self.wait(1)
        self.play(kidney.animate.shift(UP*0.2), shield.animate.shift(UP*0.2), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(banda), FadeOut(prota), FadeOut(kidney), FadeOut(shield), run_time=1)