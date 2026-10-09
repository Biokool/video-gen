from manim import *
from zenn_rig import *

class S39(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3.5 + DOWN*1.2, playera="rosa", altura=2.5, expresion="pensando", pose='de_pie')
        pantalla = caja(etiqueta="CINE", pos=RIGHT*2.0)
        mando = caja(etiqueta="MANDO", pos=RIGHT*5.0)

        self.play(FadeIn(prota), run_time=1.0)
        self.play(FadeIn(pantalla), run_time=1.0)
        self.play(FadeIn(mando), run_time=1.0)
        self.wait(8.0)