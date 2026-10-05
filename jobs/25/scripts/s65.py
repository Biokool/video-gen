from manim import *
from zenn_rig import *

class S65(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT * 2.5,
            playera="verde",
            altura=3.0,
            expresion="confundido",
            pose="senalando"
        )
        ojo = ojo_grande(pos=RIGHT * 2.5, escala=1.3, iris=TEAL)

        self.play(FadeIn(prota), FadeIn(ojo), run_time=1.0)
        self.wait(0.4)

        mirada = arrow(
            ojo.get_right(),
            RIGHT * 3.8,
            color=INK,
            width=6
        )
        self.play(Create(mirada), run_time=1.0)

        invisible = callout("INVISIBLE", color=TEAL, font_size=72)
        invisible.to_edge(UP)

        self.play(FadeIn(invisible), run_time=1.0)
        self.wait(0.6)