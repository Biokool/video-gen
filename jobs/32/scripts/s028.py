from manim import *
from zenn_rig import *

class S028(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*0.5, playera=PLAYERA_VERDE, altura=2.6,
                             expresion='pensando', pose='de_pie')
        abuela = stick_idle(pos=LEFT*3.5, height=2.0, color=INK)
        expresion(abuela, tipo='normal')
        gota = planeta(pos=RIGHT*3.5, radio=0.3, color=AZUL_MARINO)

        self.play(FadeIn(prota, shift=UP),
                  FadeIn(abuela, shift=UP),
                  Create(gota), run_time=1.5)
        self.wait(1.0)
        self.play(gota.animate.shift(DOWN*0.5), run_time=1.5)
        self.wait(2.0)
        self.wait(2.0)