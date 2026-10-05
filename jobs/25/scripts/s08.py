from manim import *
from zenn_rig import *

class S08(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*3.4 + DOWN*0.3, playera="azul",
                             expresion="sorpresa", pose="senalando")
        ojo = ojo_grande(pos=RIGHT*3.3 + UP*0.7, escala=1.1, iris=TEAL)
        det = etiqueta("detalle a detalle", (3.3, -1.6), color=INK, font_size=40)
        flecha = arrow(start=LEFT*0.9 + UP*0.3, end=RIGHT*1.7 + UP*0.6,
                       color=ORANGE, width=8)
        bcro = callout("¡Cada pelito!", color=ORANGE, font_size=96)
        bcro.shift(UP*2.4)

        self.play(FadeIn(prota, shift=RIGHT*0.4), run_time=0.9)
        self.play(FadeIn(ojo, scale=0.7), FadeIn(det), run_time=0.9)
        self.play(Create(flecha), run_time=0.7)

        cambiar_cara(prota, "alegria_pura")
        self.add(prota)
        self.play(FadeIn(bcro, scale=1.2), run_time=0.6)
        self.play(prota.animate.shift(RIGHT*0.3), run_time=0.7)
        self.wait(0.9)

        self.play(FadeOut(bcro), FadeOut(flecha), run_time=0.6)
        self.play(*[FadeOut(m) for m in [prota, ojo, det]], run_time=0.7)
        self.wait(0.2)