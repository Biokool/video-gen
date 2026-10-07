from manim import *
from zenn_rig import *

class S16(Scene):
    def construct(self):
        self.add(fondo_papel())
        prota = protagonista(DOWN*2.0+LEFT*5.0, "verde", altura=1.9,
                             expresion="pensando", pose="de_pie")
        self.play(FadeIn(prota, shift=UP*0.3), run_time=0.8)

        lineas = split_screen("SIN SABERLO", "CON SABERLO", divider_color=TEAL)
        self.play(FadeIn(lineas), run_time=1.2)

        dato = callout("¿Y si llegaran\n2 siglos antes?", color=TEAL,
                       pos=RIGHT*4.6+UP*2.7)
        self.play(FadeIn(dato, scale=1.1), run_time=0.8)

        cambiar_cara(prota, "sorpresa")
        self.play(prota.animate.shift(RIGHT*0.35), run_time=0.6)
        self.wait(1.6)