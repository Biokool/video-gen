from manim import *
from zenn_rig import *

class S15(Scene):
    def construct(self):
        # fondo nocturno violeta
        self.add(fondo(PURPLE))

        # título superior
        self.play(FadeIn(banda_titulo("INTEROCEPCI&Oacute;N", color=ORANGE)))
        self.wait(0.5)

        # personaje pensando (izquierda)
        stick = stick_idle(pos=LEFT * 3, height=2.2, color=WHITE)
        self.play(FadeIn(stick))
        self.play(FadeIn(stick_think(stick, "?")))
        self.wait(1)

        #