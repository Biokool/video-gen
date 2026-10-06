from manim import *
from zenn_rig import *

class S031(Scene):
    def construct(self):
        # protagonista principal (EL PORQUÉ) con playera roja y expresión preocupada
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_ROJA,
            altura=2.6,
            expresion='preocupado',
            pose='de_pie'
        )
        # etiquetas informativas
        txt_agua = etiqueta("80% agua", pos=(-2, 2), color=INK)
        txt_gota = etiqueta("gota ausente", pos=(-2, 0.5), color=INK)

        # animaciones
        self.play(FadeIn(prota), run_time=1.5)
        self.wait(0.5)
        self.play(Write(txt_agua), run_time=1.0)
        self.wait(0.5)
        self.play(Write(txt_gota), run_time=1.0)
        self.wait(1.0)  # total ~6 segundos