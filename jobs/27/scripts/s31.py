from manim import *
from zenn_rig import *

class S31(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=42, seed=3))
        tierra = planeta(pos=ORIGIN + UP * 0.2, radio=1.05, color=TEAL)
        prota = protagonista(pos=DOWN * 1.3 + LEFT * 3.6, playera="rosa",
                             altura=2.6, expresion="decidido", pose="senalando")
        self.play(FadeIn(tierra, scale=0.8), run_time=1.2)
        self.play(FadeIn(prota, shift=UP * 0.4), run_time=1.0)
        self.wait(0.3)
        aviso = callout("Geocentrismo:\n1400 años de error", color=CORAL,
                        font_size=52, pos=RIGHT * 3.5 + UP * 1.4)
        self.play(FadeIn(aviso, shift=LEFT * 0.3), run_time=1.0)
        self.play(Indicate(tierra, color=CORAL, scale_factor=1.15), run_time=0.9)
        self.wait(0.8)