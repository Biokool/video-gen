from manim import *
from zenn_rig import *

class S17(Scene):
    def construct(self):
        self.add(fondo(WHITE))
        prota = version_prota(5, pos=LEFT * 4 + DOWN * 0.4)
        cambiar_cara(prota, "pensando")
        ojo = ojo_grande(pos=RIGHT * 3.2 + UP * 0.4, escala=1.3, iris=TEAL)
        self.play(FadeIn(prota, shift=RIGHT * 0.5), FadeIn(ojo, scale=0.6), run_time=1.2)
        self.wait(0.3)

        c1 = callout("¿Sugestión?", color=ORANGE, font_size=72).move_to(UP * 2.9)
        self.play(FadeIn(c1, shift=DOWN * 0.3), run_time=0.6)
        self.play(Indicate(ojo, color=TEAL, scale_factor=1.15), run_time=0.8)
        self.wait(0.4)

        self.play(FadeOut(c1), run_time=0.4)
        cambiar_cara(prota, "confundido")
        c2 = callout("¿Placebo?", color=CORAL, font_size=72).move_to(UP * 2.9)
        self.play(FadeIn(c2, shift=DOWN * 0.3), run_time=0.6)
        self.wait(0.5)

        self.play(FadeOut(c2), FadeOut(ojo), run_time=0.5)
        curva_med = curva(pos=RIGHT * 3.0 + DOWN * 0.6, ancho=4.4, alto=2.2, color=INK, acento=RED)
        et = etiqueta("algo medible", (3.0, -1.9), color=INK, font_size=36)
        self.play(Create(curva_med), FadeIn(et), run_time=1.0)
        cambiar_cara(prota, "sorpresa")
        prota2 = version_prota(5, pos=LEFT * 4 + DOWN * 0.4)
        cambiar_cara(prota2, "mente_explotada")
        self.play(Transform(prota, prota2), run_time=0.6)
        self.wait(0.5)