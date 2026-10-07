from manim import *
from zenn_rig import *

class S031(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera="roja", altura=2.6, expresion='preocupado', pose='de_pie')
        brain_box = caja(etiqueta="80% agua", pos=RIGHT*3.5+UP*0.5, width=2.0)
        missing = callout(text="ausente", color=ORANGE, pos=RIGHT*3.5+UP*1.5)

        self.play(FadeIn(prota), run_time=1.0)
        self.play(FadeIn(brain_box), run_time=1.0)
        self.play(FadeIn(missing), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(prota), FadeOut(brain_box), FadeOut(missing), run_time=1.0)