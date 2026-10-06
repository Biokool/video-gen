from manim import *
from zenn_rig import *

class S047(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2 + LEFT*3.5, playera=PLAYERA_AMARILLA, altura=2.5, expresion='preocupado', pose='de_pie')
        iones_label = etiqueta("Na+ K+ desbalanceados", (2.0, 0.0))
        nervio_label = etiqueta("Nervio muscular", (-2.0, 0.0))

        self.play(FadeIn(prota), run_time=1.0)
        self.play(FadeIn(iones_label), run_time=1.0)
        self.play(FadeIn(nervio_label), run_time=1.0)
        self.wait(2.0)
        self.play(Create(red_accent(iones_label, scale=1.25)), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(prota), FadeIn(iones_label), FadeOut(nervio_label), run_time=1.0)