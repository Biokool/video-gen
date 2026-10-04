from manim import *
from zenn_rig import *

class S06(Scene):
    def construct(self):
        self.add(fondo(WHITE))
        banda = banda_titulo("LA ILUSIÓN DEL RESETEO INSTANTÁNEO", color=AZUL_MARINO)
        self.play(FadeIn(banda, shift=DOWN * 0.3), run_time=0.6)

        prota = protagonista(pos=LEFT * 3.3 + DOWN * 0.7, playera=AZUL_MARINO,
                             altura=3.0, expresion='sarcastico', pose='senalando')
        self.play(FadeIn(prota, shift=UP * 0.4), run_time=0.7)

        varita = arrow(LEFT * 1.5 + UP * 0.2, RIGHT * 0.5 + UP * 1.3, color=INK)
        self.play(Create(varita), run_time=0.6)

        chispas = VGroup(
            Star(n=5, outer_radius=0.17, color=YELLOW, fill_opacity=1).move_to(RIGHT * 0.75 + UP * 1.55),
            Star(n=5, outer_radius=0.13, color=MOSTAZA, fill_opacity=1).move_to(RIGHT * 1.25 + UP * 0.85),
            Star(n=5, outer_radius=0.11, color=ORANGE, fill_opacity=1).move_to(RIGHT * 0.15 + UP * 1.95),
            Dot(radius=0.07, color=YELLOW).move_to(RIGHT * 1.5 + UP * 1.6),
        )
        self.play(LaggedStart(*[FadeIn(c, scale=1.8) for c in chispas], lag_ratio=0.15),
                  run_time=0.7)

        etiq = etiqueta("reset instantáneo", (3.6, -1.4), color=AZUL_MARINO, font_size=34)
        self.play(FadeIn(etiq, shift=UP * 0.2), run_time=0.4)
        self.wait(0.3)

        pregunta = callout("¿MAGIA?", color=ORANGE, font_size=72).move_to(RIGHT * 4.2 + UP * 0.7)
        self.play(FadeIn(pregunta, scale=0.7), run_time=0.5)
        self.play(Indicate(chispas, scale_factor=1.3), run_time=0.5)
        self.wait(0.4)