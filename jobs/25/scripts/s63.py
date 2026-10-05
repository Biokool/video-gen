from manim import *
from zenn_rig import *

class S63(Scene):
    def construct(self):
        self.add(fondo(WHITE))

        camino_prop = camino(width=7.0, pos=DOWN * 1.8)
        casita = casa(pos=RIGHT * 5.0, size=1.0)
        ventana = caja(etiqueta="", pos=ORIGIN, width=1.8)
        stick = stick_idle(pos=LEFT * 3.4, height=2.2, color=GREEN)
        ojo = ojo_grande(pos=RIGHT * 3.2, escala=0.9, iris=TEAL)
        prota = version_prota(1, pos=ORIGIN)

        self.play(
            FadeIn(camino_prop),
            FadeIn(casita),
            FadeIn(ventana),
            FadeIn(stick),
            FadeIn(ojo),
            FadeIn(prota),
        )

        expresion(stick, "preocupado")
        self.play(stick.animate.rotate(-0.15, about_point=stick.get_bottom()))
        self.wait(2.5)