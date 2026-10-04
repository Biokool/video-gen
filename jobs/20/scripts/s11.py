from manim import *
from zenn_rig import *

class S11(Scene):
    def construct(self):
        banda = banda_titulo("MÚSCULOS DE ACERO", color=AZUL_MARINO)
        self.play(FadeIn(banda), run_time=0.6)
        prota = protagonista(LEFT*3, playera=AZUL_MARINO, expresion='decidido', pose='senalando')
        self.play(FadeIn(prota, shift=RIGHT*0.4), run_time=0.7)

        brazo = Ellipse(width=1.4, height=0.9, color=RED, fill_opacity=0.75)
        brazo.move_to(RIGHT*2.8 + UP*0.6)
        self.play(Create(brazo), run_time=0.7)

        et_flex = etiqueta("una flexión", (2.8, -1.4), color=INK)
        self.play(FadeIn(et_flex), run_time=0.4)

        self.play(brazo.animate.scale(1.35), run_time=0.7)
        self.wait(0.3)

        self.play(
            brazo.animate.scale(0.35).set_fill(opacity=0.2).set_stroke(opacity=0.4),
            run_time=0.8
        )
        cambiar_cara(prota, 'sorpresa')
        self.play(FadeOut(et_flex), run_time=0.3)

        aviso = callout("¡NO FUNCIONA ASÍ!", color=ORANGE)
        aviso.move_to(RIGHT*2.6 + UP*1.6)
        self.play(FadeIn(aviso, scale=0.8), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(aviso), FadeOut(brazo), run_time=0.5)
        self.wait(0.4)