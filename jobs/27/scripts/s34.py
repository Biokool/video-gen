from manim import *
from zenn_rig import *

class S34(Scene):
    def construct(self):
        self.add(fondo_papel())
        prota = protagonista(pos=DOWN * 1.4 + LEFT * 3.6, playera="teal",
                             altura=2.6, expresion="feliz", pose="senalando")
        boton = RoundedRectangle(corner_radius=0.32, width=3.2, height=1.0)
        boton.set_fill(RED, opacity=1).set_stroke(WHITE, width=6)
        boton.move_to(RIGHT * 3.6 + UP * 1.0)
        txt = Text("SUSCRIBIRSE", font_size=34, color=WHITE, weight=BOLD)
        txt.move_to(boton.get_center())
        flecha = arrow(start=LEFT * 1.5 + DOWN * 0.5,
                       end=RIGHT * 1.7 + UP * 0.7, color=INK)

        self.play(FadeIn(prota, shift=RIGHT * 0.6), run_time=0.9)
        self.play(FadeIn(boton, scale=0.85), Write(txt), run_time=0.9)
        self.play(Create(flecha), run_time=0.6)
        self.play(Indicate(boton, color=YELLOW, scale_factor=1.15), run_time=0.7)
        cambiar_cara(prota, "alegria_pura")
        self.play(Flash(boton.get_center(), color=YELLOW, line_length=0.35,
                        num_lines=14, flash_radius=1.1), run_time=0.6)
        self.wait(0.4)