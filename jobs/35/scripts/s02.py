from manim import *
from zenn_rig import *

class S02(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=42, seed=7, color=WHITE))

        protagonista_principal = version_prota(1, pos=DOWN*1.2+LEFT*3.5, altura=2.6)
        self.play(FadeIn(protagonista_principal))

        mano_roja = Line(ORIGIN, DOWN*1.5, stroke_color=RED, stroke_width=15)
        mano_azul = Line(ORIGIN, DOWN*1.5, stroke_color=BLUE, stroke_width=15)
        mano_roja.move_to(RIGHT*2)
        mano_azul.move_to(LEFT*2)

        self.play(
            protagonista_principal.animate.set_expression("pensando"),
            Create(mano_roja),
            Create(mano_azul)
        )
        self.wait(1)

        callout_texto = "¿Por qué hay zurdos y diestros?"
        callout_obj = callout(callout_texto, color=ORANGE, pos=RIGHT*3.4+UP*1)
        self.play(FadeIn(callout_obj))
        self.wait(3)

        self.play(
            protagonista_principal.animate.set_expression("mente_explotada"),
            FadeOut(mano_roja),
            FadeOut(mano_azul),
            FadeOut(callout_obj)
        )
        self.wait(2)

        self.play(
            protagonista_principal.animate.set_expression("normal"),
            FadeOut(protagonista_principal)
        )
        self.wait(1)