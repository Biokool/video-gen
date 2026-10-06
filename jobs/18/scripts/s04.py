from manim import *
from zenn_rig import *

class S04(Scene):
    def construct(self):
        # Protagonist with blue shirt, thinking pose, pointing
        prota = protagonista(pos=LEFT*2 + DOWN*0.5, playera=PLAYERA_AZUL,
                             altura=3.0, expresion='pensando', pose='senalando')
        # Callout highlighting the key term
        callout_ip = callout(text="ipRGC", color=ORANGE, font_size=96)
        callout_ip.shift(UP*2)
        # Small red brain representing the suprachiasmatic nucleus
        cerebro = planeta(pos=RIGHT*2 + DOWN*0.5, radio=0.5, color=RED)
        # Blue arrow from the protagonist's eye to the brain
        eye_start = prota.get_center() + UP*0.5 + LEFT*0.3
        arrow_brain = arrow(start=eye_start, end=cerebro.get_center(),
                            color=BLUE, width=8)
        # Entrance animations
        self.play(FadeIn(prota), FadeIn(callout_ip), FadeIn(cerebro), run_time=2)
        self.wait(1)
        # Arrow growth to show signal transmission
        self.play(Create(arrow_brain), run_time=3)
        self.wait(2)
        # Emphasize the brain with a red accent (using animate)
        self.play(cerebro.animate.set_color(RED).scale(1.3), run_time=1.5)
        self.wait(2)
        # Exit animations
        self.play(FadeOut(prota), FadeOut(callout_ip),
                  FadeOut(cerebro), FadeOut(arrow_brain), run_time=2)
        self.wait(1)