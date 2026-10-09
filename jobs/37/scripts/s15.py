from manim import *
from zenn_rig import *

class S15(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        banda = banda_titulo("¿Bronce o Vikinga?", color=ORANGE)
        self.play(FadeIn(banda, shift=DOWN*0.3), run_time=0.5)

        prota = protagonista(pos=DOWN*1.2 + LEFT*3.5, playera="azul", altura=2.6, expresion="sorpresa")
        self.play(FadeIn(prota, shift=UP*0.3), run_time=0.5)

        etiqueta_bronce = etiqueta("Edad del Bronce", RIGHT*1.5 + UP*1.2, color=INK)
        etiqueta_vikinga = etiqueta("Era Vikinga", RIGHT*1.5 + DOWN*0.8, color=INK)

        self.play(Write(etiqueta_bronce), run_time=0.6)
        self.play(Write(etiqueta_vikinga), run_time=0.6)

        caja_bronce = caja("Bronce", pos=RIGHT*3.8 + UP*1.2, width=1.5)
        caja_vikinga = caja("Vikinga", pos=RIGHT*3.8 + DOWN*0.8, width=1.5)
        self.play(FadeIn(caja_bronce, scale=0.8), FadeIn(caja_vikinga, scale=0.8), run_time=0.6)

        flecha = arrow(LEFT*3.0 + DOWN*1.0, RIGHT*2.5 + UP*1.0, color=RED, width=6)
        self.play(Create(flecha), run_time=0.8)

        cambiar_cara(prota, "feliz")
        self.play(prota.animate.shift(RIGHT*0.3), run_time=0.4)
        self.wait(0.6)

        self.play(
            FadeOut(banda),
            FadeOut(prota),
            FadeOut(etiqueta_bronce),
            FadeOut(etiqueta_vikinga),
            FadeOut(caja_bronce),
            FadeOut(caja_vikinga),
            FadeOut(flecha),
            run_time=0.5
        )