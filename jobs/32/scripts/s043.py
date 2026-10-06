from manim import *
from zenn_rig import *

class S043(Scene):
    def construct(self):
        # Protagonista con playera amarilla y expresión triste
        prota = protagonista(
            pos=DOWN*0.5,
            playera="amarilla",
            altura=2.6,
            expresion="triste",
            pose="de_pie"
        )
        # Corazón protegido (representado con una caja y símbolo)
        corazon = caja("♥", pos=LEFT*2, width=1.5)
        # Célula agotada (representada con una caja y texto)
        celula = caja("célula", pos=RIGHT*2, width=1.5)

        self.play(FadeIn(prota), FadeIn(corazon), FadeIn(celula))
        self.wait(0.5)
        self.play(FadeOut(prota), FadeOut(corazon), FadeOut(celula))
        self.wait(0.5)  # total ~2 seconds