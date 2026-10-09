from manim import *
from zenn_rig import *

class S29(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*2, playera="roja", altura=3.0, expresion='pensando', pose='de_pie')
        casco = casco_vikingo(pos=RIGHT*2 + UP*0.5, escala=1.0)
        self.play(FadeIn(prota), FadeIn(casco), run_time=1.5)
        self.wait(1)
        cambiar_cara(prota, 'decidido')
        self.wait(1)
        note = callout("Cascos con cuernos", color=ORANGE, pos=RIGHT*4+UP*1)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(1)
        self.play(FadeIn(red_accent(casco, scale=1.25)), run_time=0.5)
        self.wait(1.5)
        self.play(casco.animate.shift(UP*0.2), run_time=0.5)
        self.wait(2)