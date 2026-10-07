from manim import *
from zenn_rig import *

class S17(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=42, seed=7, color=WHITE))

        banda = banda_titulo("1543 · Copérnico", color=YELLOW)
        self.play(FadeIn(banda, shift=DOWN * 0.2), run_time=0.6)

        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 4.3,
            playera="roja",
            altura=2.5,
            expresion="sorpresa",
            pose="senalando",
        )
        self.play(FadeIn(prota, shift=UP * 0.3), run_time=0.7)

        centro = RIGHT * 1.5 + UP * 1.0
        sol_obj = sol(color=YELLOW, radius=0.65, pos=centro)
        self.play(Create(sol_obj), run_time=0.8)

        orbita = Circle(radius=1.75, color=WHITE, stroke_opacity=0.35).move_to(centro)
        tierra = planeta(pos=centro + RIGHT * 1.75, radio=0.30, color=TEAL)
        self.play(Create(orbita), FadeIn(tierra), run_time=0.9)

        self.play(Rotate(tierra, angle=2 * PI, about_point=centro), run_time=4.2)

        # red_accent devuelve un Mobject (no una animación): hay que envolverlo
        acento = red_accent(sol_obj, scale=1.15)
        self.play(FadeIn(acento), run_time=0.4)
        self.play(FadeOut(acento), run_time=0.4)

        nota = etiqueta(
            "La Tierra gira alrededor del Sol",
            pos=RIGHT * 3.4 + DOWN * 1.8,
            color=ORANGE,
            font_size=36,
        )
        self.play(FadeIn(nota, shift=UP * 0.2), run_time=0.8)

        cambiar_cara(prota, "alegria_pura")
        self.play(prota.animate.shift(RIGHT * 0.25), run_time=0.6)
        self.wait(1.2)