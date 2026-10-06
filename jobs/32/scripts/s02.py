from manim import *
from zenn_rig import *

class S02(Scene):
    def construct(self):
        # posición base del protagonista
        prota_pos = DOWN*0.5 + LEFT*3.5

        # protagonista (conductor)
        prota = protagonista(
            pos=prota_pos,
            playera=PLAYERA_NARANJA,
            altura=2.5,
            expresion="pensando",
            pose="senalando"
        )

        # cama a la derecha
        cama = caja(etiqueta="", pos=DOWN*0.5 + RIGHT*3.5, width=2.8)

        # gota azul sobre el protagonista
        gota = caja(etiqueta="", pos=prota_pos + UP*0.2 + RIGHT*0.2, width=0.2)
        gota.set_color(BLUE_E)
        gota.set_fill(opacity=0.8)

        # animaciones
        self.play(FadeIn(prota), FadeIn(cama), run_time=1.5)
        self.play(Create(gota), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(gota), run_time=0.5)
        self.wait(2.5)