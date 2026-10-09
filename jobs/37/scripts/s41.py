from manim import *
from zenn_rig import *

class S41(Scene):
    def construct(self):
        banda = banda_titulo("¿HISTORIA O HOLLYWOOD?", color=ORANGE)
        prota = protagonista(
            pos=DOWN * 1.2 + LEFT * 3.5,
            playera="amarilla",
            altura=2.4,
            expresion="confundido",
            pose="senalando",
        )
        logo = etiqueta("HOLLYWOOD", (3.2, 0.4), color=YELLOW, font_size=56, ancho_max=4.6)
        luces = VGroup(
            etiqueta("•", (1.7, 1.4), color=RED, font_size=38, ancho_max=0.8),
            etiqueta("•", (4.7, 1.4), color=TEAL, font_size=38, ancho_max=0.8),
            etiqueta("•", (1.9, -0.5), color=ORANGE, font_size=34, ancho_max=0.8),
            etiqueta("•", (4.5, -0.5), color=YELLOW, font_size=34, ancho_max=0.8),
        )
        self.play(FadeIn(banda), FadeIn(prota, shift=UP * 0.25), run_time=1.3)
        self.play(FadeIn(logo), run_time=0.7)
        self.play(FadeIn(luces, lag_ratio=0.12), run_time=0.8)
        self.play(Indicate(logo, color=RED, scale_factor=1.08), run_time=0.8)
        self.play(
            logo.animate.set_color(TEAL),
            luces[0].animate.set_color(TEAL),
            luces[2].animate.set_color(RED),
            run_time=0.5,
        )
        self.play(
            logo.animate.set_color(ORANGE),
            luces[1].animate.set_color(YELLOW),
            luces[3].animate.set_color(TEAL),
            run_time=0.5,
        )
        prota_nueva_cara = cambiar_cara(prota, "sorpresa")
        self.play(ReplacementTransform(prota, prota_nueva_cara), run_time=0.6)
        self.play(Indicate(logo, color=ORANGE, scale_factor=1.05), run_time=0.8)
        self.wait(0.9)
        self.play(logo.animate.set_color(YELLOW), run_time=0.4)
        self.wait(0.7)