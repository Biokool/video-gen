from manim import *
from zenn_rig import *

class S97(Scene):
    def construct(self):
        self.add(fondo(INK))
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_NARANJA, altura=2.6, expresion='pensando', pose='de_pie')
        self.add(prota)
        self.wait(2)
        pianista = stick_idle(pos=RIGHT*3.5, height=2.2, color=WHITE)
        self.add(pianista)
        self.wait(1)
        self.play(pianista.animate.shift(RIGHT*3.5+UP*1-RIGHT*3.5), run_time=2.0)
        self.wait(1)
        callout_text = callout("¿Qué es más 'tú'?", color=ORANGE, font_size=60, ancho_max=7.0, pos=RIGHT*3.4+UP*1)
        self.add(callout_text)
        self.wait(2)
        self.play(FadeOut(callout_text))
        self.wait(1)
        self.play(pianista.animate.set_position(RIGHT*3.5+UP*1))
        self.wait(2)
        self.play(FadeOut(pianista), FadeOut(prota))
        self.wait(1)