from manim import *
from zenn_rig import *

class S83(Scene):
    def construct(self):
        prota = protagonista(LEFT * 3.0, playera='rosa', expresion='pensando', pose='de_pie')
        self.play(FadeIn(prota, run_time=0.7))

        ojo = ojo_grande(RIGHT * 3.0, escala=1.0, iris=TEAL)
        self.play(FadeIn(ojo, run_time=0.7))

        cerebro = sol(color=YELLOW, radius=0.6, pos=UP * 1.5 + RIGHT * 1.8)
        self.play(FadeIn(cerebro, run_time=0.7))

        conexion = arrow(cerebro.get_center(), ojo.get_center(), color=YELLOW, width=8)
        self.play(Create(conexion, run_time=1.0))

        mensaje = callout("COMPRENDER", color=ORANGE, font_size=72)
        mensaje.move_to(UP * 3.0)
        self.play(Write(mensaje, run_time=0.8))
        self.wait(0.8)