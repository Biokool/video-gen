from manim import *
from zenn_rig import *

class S27(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        prota = version_prota(7, pos=DOWN*1.2 + LEFT*3.5, altura=2.4)
        self.play(FadeIn(prota), run_time=0.8)
        etiqueta_wagner = etiqueta("Richard Wagner", pos=RIGHT*3.4 + UP*1)
        self.play(FadeIn(etiqueta_wagner), run_time=0.8)
        self.wait(1.0)
        self.play(prota.animate.shift(RIGHT*0.5), run_time=0.6)
        self.play(prota.animate.shift(RIGHT*1.5), run_time=1.2)
        self.wait(0.5)
        etiqueta_doelper = etiqueta("Carl Emil Doepler", pos=RIGHT*3.4 + DOWN*0.5)
        self.play(FadeIn(etiqueta_doelper), run_time=0.8)
        self.wait(1.0)
        self.play(
            FadeOut(etiqueta_wagner),
            FadeOut(etiqueta_doelper),
            FadeOut(prota),
            run_time=0.8
        )
        self.wait(0.5)