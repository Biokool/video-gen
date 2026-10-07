from manim import *
from zenn_rig import *


class S28(Scene):
    def construct(self):
        self.add(fondo_papel())

        banda = banda_titulo("Cronometría → Revolución Industrial", color=ORANGE)
        self.play(FadeIn(banda))

        prota = protagonista(DOWN * 1.2 + LEFT * 3.5, playera="amarilla",
                             altura=2.6, expresion="sorpresa", pose="senalando")
        self.play(FadeIn(prota))

        globo = planeta(RIGHT * 3.6 + UP * 0.1, radio=0.9, color=TEAL)
        self.play(Create(globo))

        moneda = moneda_dorada("$", pos=RIGHT * 2.0 + DOWN * 1.0, radio=0.55)
        fuego1 = fuego(pos=RIGHT * 5.1 + DOWN * 1.0, escala=0.7)
        self.play(FadeIn(moneda), FadeIn(fuego1))

        dato = etiqueta("Comercio global", pos=RIGHT * 3.6 + UP * 1.7, color=ORANGE)
        self.play(FadeIn(dato))

        self.play(Indicate(globo, color=RED, scale_factor=1.2), run_time=0.8)

        cambiar_cara(prota, "euforico")
        self.wait(1.2)