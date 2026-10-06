from manim import *
from zenn_rig import *

class S050(Scene):
    def construct(self):
        prota = protagonista(pos=ORIGIN,
                             playera=PLAYERA_AMARILLA,
                             altura=2.6,
                             expresion='pregunta',
                             pose='de_pie')
        mensaje_caja = caja(etiqueta="Mensaje", pos=RIGHT*2.5, width=1.5)
        signo_interrogacion = etiqueta("?", pos=LEFT*2.5 + UP*1.0)

        self.play(FadeIn(prota), run_time=1.5)
        self.play(Create(mensaje_caja), run_time=1.5)
        self.play(Write(signo_interrogacion), run_time=1.5)
        self.wait(1.5)