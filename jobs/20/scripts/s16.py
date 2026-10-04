from manim import *
from zenn_rig import *

class S16(Scene):
    def construct(self):
        # Fondo claro (por defecto)
        prota = protagonista(
            LEFT * 3,
            playera=AZUL_MARINO,
            altura=3.0,
            expresion="pensando",
            pose="de_pie",
        )
        self.play(FadeIn(prota, scale=0.8))
        self.wait(0.5)

        energia = curva(
            pos=prota.get_center() + UP * 0.8,
            ancho=3.2,
            alto=1.4,
            color=TEAL,
            acento=RED,
        )
        self.play(Create(energia, run_time=1.2))
        self.wait(0.3)

        mensaje = callout(
            "Ese “respiro” no cambia el cableado,\npero sí la energía que fluye",
            color=ORANGE,
            font_size=96,
        )
        mensaje.move_to(UP * 2.2)
        self.play(FadeIn(mensaje, scale=0.9), run_time=0.8)
        self.wait(1.0)

        # Cerrar con fade out
        self.play(
            FadeOut(mensaje),
            FadeOut(energia),
            FadeOut(prota),
            run_time=1.2,
        )
        self.wait(0.5)