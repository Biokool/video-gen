from manim import *
from zenn_rig import *

class S12(Scene):
    def construct(self):
        prota = protagonista(pos=RIGHT*3.0+UP*0.6, playera=PLAYERA_NARANJA,
                             expresion='decidido', pose='brazos_cruzados')
        self.play(FadeIn(prota, shift=UP*0.4), run_time=0.6)

        cerebro = VGroup(
            Ellipse(width=1.1, height=1.6).set_fill("#E8A0B0", 1).set_stroke(INK, 3).shift(LEFT*0.5),
            Ellipse(width=1.1, height=1.6).set_fill("#E8A0B0", 1).set_stroke(INK, 3).shift(RIGHT*0.5),
        ).move_to(LEFT*2.6 + UP*0.9)

        boton = Circle(radius=0.32, color=INK, stroke_width=3)
        boton.set_fill("#9AA0A6", 1).move_to(LEFT*2.6 + DOWN*0.55)
        etq = etiqueta("REINICIO TOTAL", (-2.6, -1.5), color=INK, font_size=32)
        tachado = Line(boton.get_corner(UL)+UL*0.08, boton.get_corner(DR)+DR*0.08,
                       color=RED, stroke_width=9)

        self.play(Create(cerebro), run_time=0.8)
        self.play(FadeIn(boton), FadeIn(etq), run_time=0.4)
        self.play(Create(tachado), run_time=0.6)

        flecha = arrow(prota.get_left()+LEFT*0.2+UP*0.4, cerebro.get_right()+RIGHT*0.15)
        self.play(Create(flecha), run_time=0.5)

        aviso = callout("SIN REINICIO", color=ORANGE).move_to(UP*2.7)
        self.play(Write(aviso), run_time=0.8)

        realce = red_accent(tachado)
        self.play(Create(realce), run_time=0.4)
        self.wait(1.2)