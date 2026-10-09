from manim import *
from zenn_rig import *

class S35(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(30, seed=35))
        self.add(luna(pos=RIGHT*4 + UP*2.5, radio=0.6))

        banda = banda_titulo("¡Mitos vikingos!", color=ORANGE)
        self.play(FadeIn(banda, shift=DOWN*0.5), run_time=0.6)

        prota = version_prota(4, pos=DOWN*1.4 + LEFT*3.2)
        self.play(FadeIn(prota, shift=RIGHT*0.5), run_time=0.8)

        casco = casco_vikingo(pos=DOWN*1.0 + RIGHT*2.8, escala=2.2)
        self.play(Create(casco), run_time=0.7)

        call = etiqueta("MÁS COOL = MÁS MEMORABLE", pos=RIGHT*3.6 + UP*0.8, color=ORANGE, font_size=40)
        self.play(FadeIn(call, shift=DOWN*0.3), run_time=0.6)

        self.wait(1.8)

        # Se corrige el error usando Transform, ya que cambiar_cara devuelve un VGroup
        self.play(Transform(prota, cambiar_cara(prota, "feliz")), run_time=0.2)
        self.play(FadeOut(call), run_time=0.5)
        self.wait(2.0)

        self.play(
            FadeOut(banda),
            FadeOut(prota),
            FadeOut(casco),
            run_time=0.6
        )
        self.wait(0.3)