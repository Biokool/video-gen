from manim import *
from zenn_rig import *

class S02(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(30, seed=3))
        self.add(luna(pos=RIGHT*4+UP*2.5, radio=0.8))

        banda = banda_titulo("¿CUERNOS VIKINGOS?", color=ORANGE)
        self.play(FadeIn(banda), run_time=0.6)

        prota = protagonista(
            pos=DOWN*0.8 + LEFT*3.2,
            playera="naranja",
            altura=2.4,
            expresion="sorpresa",
            pose="senalando"
        )
        self.play(FadeIn(prota, shift=RIGHT*0.3), run_time=0.8)
        self.wait(0.4)

        casco = casco_vikingo(pos=RIGHT*2.5 + UP*0.3, escala=1.1)
        self.play(FadeIn(casco, scale=0.7), run_time=0.7)
        self.wait(0.3)

        tachado = red_accent(casco, scale=1.3)
        self.play(Create(tachado), run_time=0.8)
        self.wait(0.5)

        call = etiqueta("0 cascos reales", pos=RIGHT*2.5 + DOWN*1.0, color=RED)
        self.play(FadeIn(call), run_time=0.6)
        self.wait(0.5)

        cambiar_cara(prota, "alegria_pura")
        self.wait(0.5)

        self.play(FadeOut(tachado), run_time=0.5)
        self.wait(0.4)

        etq = etiqueta("Disfraz moderno", pos=RIGHT*2.5 + UP*1.4, color=ORANGE)
        self.play(Transform(call, etq), run_time=0.7)
        self.wait(0.6)

        self.play(FadeOut(call), FadeOut(casco), run_time=0.6)
        self.wait(0.3)

        self.play(FadeOut(banda), run_time=0.5)
        self.wait(0.3)