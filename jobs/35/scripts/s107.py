from manim import *
from zenn_rig import *

class S107(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT*3.5+DOWN*0.5,
            playera=PLAYERA_NARANJA,
            altura=2.6,
            expresion='pensando',
            pose='de_pie'
        )
        lupa_obj = lupa(
            pos=LEFT*2.0+DOWN*0.5,
            escala=0.8,
            color=INK
        )
        callout_obj = callout(
            text="Corballis 2017",
            color=ORANGE,
            font_size=48,
            pos=RIGHT*3.4+DOWN*0.5
        )

        self.play(FadeIn(prota), run_time=1.5)
        self.play(FadeIn(lupa_obj), run_time=1.0)
        self.play(FadeIn(callout_obj), run_time=1.0)
        self.wait(2.0)