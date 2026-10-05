from manim import *
from zenn_rig import *

class S16(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        prota = protagonista(pos=LEFT * 4.5, playera="azul", altura=3.0, expresion="sorpresa", pose="senalando")
        ojo = ojo_grande(pos=LEFT * 0.6 + UP * 1.2, escala=1.1, iris=TEAL)
        punto = Dot(point=RIGHT * 5.4, radius=0.07, color=INK)
        trail = DashedLine(RIGHT * 2.2 + DOWN * 0.3, RIGHT * 5.1 + DOWN * 0.3, stroke_width=2, color=GREY, dash_length=0.15)

        self.play(FadeIn(prota), run_time=0.8)
        self.play(FadeIn(ojo), Create(trail), run_time=0.8)
        self.play(FadeIn(punto), run_time=0.5)
        cambiar_cara(prota, "confundido")
        self.play(punto.animate.scale(2.0).set_color(RED), run_time=0.5)
        et = etiqueta("la hormiga", (5.0, 0.9), color=RED, font_size=36, ancho_max=3.0)
        self.play(FadeIn(et), run_time=0.4)
        self.wait(0.8)