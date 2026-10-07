from manim import *
from zenn_rig import *

class S23(Scene):
    def construct(self):
        self.add(fondo_papel())

        prota = protagonista(pos=LEFT*3.6+DOWN*0.4, playera="roja",
                             altura=2.7, expresion="enojado",
                             pose="brazos_cruzados")
        reloj = reloj_pared(radius=0.9, pos=RIGHT*3.6+DOWN*1.7)

        self.play(FadeIn(prota, shift=UP*0.4), Create(reloj), run_time=1.2)

        q = callout("¿Por qué tardó\nmás de un siglo?", color=RED,
                    font_size=52, pos=RIGHT*3.3+UP*1.5)
        self.play(FadeIn(q, scale=1.2), run_time=0.8)

        cambiar_cara(prota, "confundido")
        self.play(prota.animate.shift(RIGHT*0.35), run_time=0.6)

        cambiar_cara(prota, "enojado")
        self.play(Indicate(q, color=RED, scale_factor=1.12), run_time=0.9)

        self.play(Indicate(reloj, color=RED, scale_factor=1.15), run_time=1.0)

        self.wait(2.0)