from manim import *
from zenn_rig import *

class S32(Scene):
    def construct(self):
        # Protagonista como conductor de la escena
        prota = protagonista(
            pos=LEFT * 3.4 + DOWN * 0.4,
            playera=PLAYERA_ROJA,
            expresion="sorpresa",
            pose="senalando"
        )
        self.add(prota)
        self.play(FadeIn(prota, scale=0.8), run_time=0.7)
        self.wait(0.3)

        celula = planeta(pos=RIGHT * 2.8 + UP * 0.2, radio=2.3, color=CREMA)
        self.play(Create(celula), run_time=0.8)
        self.wait(0.2)

        nucleo = ojo_grande(pos=RIGHT * 2.4 + UP * 0.5, escala=0.9, iris=TEAL)
        mito = matraz(pos=RIGHT * 3.4 + DOWN * 0.6, escala=0.7, liquido=CORAL)
        reticulo = curva(
            pos=RIGHT * 2.0 + DOWN * 0.2,
            ancho=1.6,
            alto=1.1,
            color=INK,
            acento=RED
        )

        self.play(
            FadeIn(nucleo, scale=0.5),
            FadeIn(mito, scale=0.5),
            FadeIn(reticulo, scale=0.5),
            run_time=0.9
        )
        self.wait(0.3)

        # El protagonista reacciona y señala la célula
        self.play(prota.animate.shift(UP * 0.1), run_time=0.2)

        self.play(
            FadeIn(callout("¡ORGANELOS!", color=ORANGE, font_size=72).to_edge(UP)),
            run_time=0.7
        )
        self.wait(0.5)

        etiqueta("núcleo", (2.4, 1.5))
        etiqueta("mitocondria", (3.8, -1.3))
        etiqueta("retículo", (0.8, -1.2))
        self.wait(0.5)

        self.play(
            FadeOut(celula),
            FadeOut(nucleo),
            FadeOut(mito),
            FadeOut(reticulo),
            FadeOut(prota),
            run_time=0.6
        )
        self.wait(0.2)