from manim import *
from zenn_rig import *

class S44(Scene):
    def construct(self):
        self.add(fondo_papel())

        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_VERDE, altura=2.6, expresion='sorpresa', pose='senalando')
        libro = caja(etiqueta="Cuentos", pos=RIGHT*2.5+DOWN*0.5, width=2.0)
        antorcha = vela(pos=prota.get_center()+RIGHT*0.8+UP*0.5, escala=1.2)

        self.play(FadeIn(prota), Create(libro))
        self.wait(0.5)
        self.play(FadeIn(antorcha))
        self.wait(1.0)

        self.play(prota.animate.shift(RIGHT*0.5), run_time=1.5)
        self.wait(1.0)
        callout("Ficción > Realidad", pos=RIGHT*3.4+UP*1)
        self.wait(3.0)

        self.play(FadeOut(prota), FadeOut(libro), FadeOut(antorcha))
        self.wait(0.5)