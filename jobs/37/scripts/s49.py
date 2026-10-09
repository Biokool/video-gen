from manim import *
from zenn_rig import *

class S49(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(20, seed=49, color=WHITE))

        banda = banda_titulo("Carl Emil Doepler", color=ORANGE)
        self.play(FadeIn(banda, shift=DOWN*0.3), run_time=0.6)

        prota = protagonista(pos=LEFT*3.5+DOWN*1.2, playera="teal", altura=2.6, expresion="sorpresa", pose="senalando")
        self.play(FadeIn(prota, shift=UP*0.4), run_time=0.7)

        vikingo = personaje(pos=RIGHT*3.2+DOWN*1.0, cuerpo=AZUL_MARINO, altura=2.2, expresion_tipo="normal")
        casco = casco_vikingo(pos=RIGHT*3.2+UP*0.5, escala=0.8)
        self.play(FadeIn(vikingo, shift=LEFT*0.4), FadeIn(casco, scale=0.8), run_time=0.7)

        self.wait(1.2)
        cambiar_cara(prota, "euforico")
        self.wait(0.5)
        self.play(FadeOut(banda), run_time=0.4)