from manim import *
from zenn_rig import *

class S14(Scene):
    def construct(self):
        prota = protagonista(
            pos=DOWN*1.2,
            playera=PLAYERA_NARANJA,
            altura=2.5,
            expresion='sorpresa',
            pose='de_pie'
        )
        helmet = casco_vikingo(escala=1.3)
        warning = Text("!", font_size=30, color=RED)

        # Position helmet to the left of the protagonist and warning to the right
        helmet.next_to(prota, LEFT, buff=0.5)
        warning.next_to(prota, RIGHT, buff=0.5)

        self.play(FadeIn(prota), FadeIn(helmet), FadeIn(warning))
        self.wait(2)

        # Slight downward shift for all elements
        self.play(
            prota.animate.shift(DOWN*0.2),
            helmet.animate.shift(DOWN*0.2),
            warning.animate.shift(DOWN*0.2)
        )
        self.wait(2)