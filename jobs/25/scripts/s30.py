from manim import *
from zenn_rig import *

class S30(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT * 4,
            playera='rosa',
            altura=3.0,
            expresion='feliz',
            pose='de_pie'
        )
        celula = ojo_grande(pos=RIGHT * 3.5, escala=1.2, iris=TEAL)
        medida = etiqueta("10-100 µm", (3.5, 1.8), font_size=36)

        self.play(FadeIn(prota, shift=UP * 0.3))
        self.play(Create(celula), run_time=1.0)
        self.play(Write(medida), run_time=0.8)
        cambiar_cara(prota, 'sorpresa')
        self.wait(1.2)