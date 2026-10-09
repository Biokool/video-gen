from manim import *
from zenn_rig import *

class S59(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT*3.5,
            playera=PLAYERA_NARANJA,
            altura=3.0,
            expresion='pensando',
            pose='de_pie'
        )
        art_vs_history = callout(
            "El arte eclipsa la historia, creando un mito",
            color=ORANGE,
            font_size=48,
            pos=RIGHT*3.4+UP*1
        )
        self.play(FadeIn(prota), FadeIn(art_vs_history))
        self.wait(1.5)
        cambiar_cara(prota, 'sorpresa')
        self.wait(1.5)
        self.play(FadeOut(prota), FadeOut(art_vs_history))
        self.wait(0.5)