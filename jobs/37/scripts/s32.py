from manim import *
from zenn_rig import *

class S32(Scene):
    def construct(self):
        banda = banda_titulo("IMPACTO VISUAL", color=ORANGE)
        self.play(FadeIn(banda, shift=DOWN*0.5), run_time=0.8)

        # Se reduce la altura a 2.6 para evitar que la cabeza colisione con la banda superior
        proto = version_prota(5, pos=DOWN*1.2 + LEFT*3.5, altura=2.6)
        cambiar_cara(proto, "sorpresa")
        self.play(FadeIn(proto, shift=UP*0.4), run_time=0.8)

        casco = casco_vikingo(pos=RIGHT*3.2 + UP*0.3, escala=2.4)
        self.play(FadeIn(casco, shift=LEFT*0.4), run_time=1.0)

        etq = etiqueta("UN DISEÑADOR REESCRIBIÓ UNA CIVILIZACIÓN", pos=(RIGHT*3.4 + DOWN*1.2), color=YELLOW)
        self.play(FadeIn(etq, shift=UP*0.3), run_time=0.8)
        self.wait(4.5)

        self.play(FadeOut(etq), run_time=0.6)
        self.play(FadeOut(casco, shift=RIGHT*0.4), run_time=0.8)
        self.play(FadeOut(banda, shift=UP*0.5), FadeOut(proto, shift=DOWN*0.3), run_time=0.6)
        self.wait(0.4)