from manim import *
from zenn_rig import *

class S22(Scene):
    def construct(self):
        self.add(fondo(AZUL_MARINO))
        prota = protagonista(DOWN*1.4+LEFT*3.6, "roja", altura=2.6, expresion="triste")
        cruz = VGroup(
            Line(UP*0.9, DOWN*0.9, color=CREMA, stroke_width=9),
            Line(LEFT*0.55, RIGHT*0.55, color=CREMA, stroke_width=9),
        )
        cruz[1].shift(UP*0.25)
        cruz.move_to(RIGHT*1.5+UP*0.1)
        libro = caja("DIÁLOGO", pos=RIGHT*3.9+DOWN*0.5, width=1.7)
        tachon = Line(
            libro.get_corner(UL)+LEFT*0.12,
            libro.get_corner(DR)+RIGHT*0.12,
            color=CORAL, stroke_width=9,
        )
        dato = callout("1633: prohibida hasta 1758", color=CORAL,
                       font_size=44, pos=RIGHT*3.4+UP*2.4)

        self.play(FadeIn(prota), run_time=0.6)
        self.play(Create(cruz), run_time=0.5)
        self.play(FadeIn(libro, shift=UP*0.3), run_time=0.5)
        self.play(Create(tachon), run_time=0.6)
        self.play(FadeIn(dato, shift=DOWN*0.2), run_time=0.6)
        self.play(Indicate(prota, color=RED), run_time=1.0)
        self.wait(4.0)