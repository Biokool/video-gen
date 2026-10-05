from manim import *
from zenn_rig import *

class S25(Scene):
    def construct(self):
        self.add(fondo(INK))
        est = estrellas(n=44, seed=11, color=WHITE)

        prota = protagonista(pos=LEFT*3.7 + DOWN*0.3, playera="azul",
                             altura=3.0, expresion="sorpresa", pose="senalando")
        cambiar_cara(prota, "sorpresa")

        ojo = ojo_grande(pos=RIGHT*3.5 + UP*1.1, escala=0.85, iris=CORAL)
        plan = planeta(pos=RIGHT*5.0 + DOWN*0.9, radio=0.75, color=TEAL)
        curv = curva(pos=RIGHT*1.0 + DOWN*1.1, ancho=2.6, alto=1.5)
        cel = dino(pos=RIGHT*1.9 + UP*2.4, color=MOSTAZA, escala=0.5)

        self.play(FadeIn(est, shift=UP*0.3), run_time=0.6)
        self.play(FadeIn(prota, shift=UP*0.4), run_time=0.8)
        self.play(FadeIn(ojo, scale=1.4), GrowFromCenter(plan),
                  Create(curv), FadeIn(cel), run_time=1.2)

        co = callout("¡Otro universo!", color=CORAL, font_size=76)
        self.play(FadeIn(co, scale=1.15), run_time=0.7)
        self.play(prota.animate.shift(RIGHT*0.6 + UP*0.2),
                  ojo.animate.shift(DOWN*0.3), run_time=1.0)
        cambiar_cara(prota, "alegria_pura")
        self.play(FadeOut(co), run_time=0.5)
        self.wait(0.4)