from manim import *
from zenn_rig import *

class S90(Scene):
    def construct(self):
        # Protagonista colocado a la izquierda y abajo para evitar solapamiento
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_NARANJA,
            altura=2.6,
            expresion='pensando',
            pose='de_pie'
        )
        # Dino inicial a la derecha (usamos nombre distinto para evitar colisión con la función dino)
        dino_fig = dino(pos=RIGHT*2, color=TEAL, escala=1.2)
        # Callout en el lado opuesto (derecha) y ligeramente arriba
        callout_txt = callout(
            "Y si miramos aún más atrás, a la evolución, la lateralidad podría tener ventajas",
            color=ORANGE,
            pos=RIGHT*3.5 + UP*0.5
        )

        self.play(FadeIn(prota), FadeIn(dino_fig), run_time=1.5)
        self.wait(2)
        self.play(FadeIn(callout_txt), run_time=1)
        self.wait(4)
        self.play(dino_fig.animate.shift(RIGHT*1.5), run_time=2)
        self.wait(5)
        cambiar_cara(prota, 'decidido')
        self.wait(4)
        self.play(FadeOut(prota), FadeOut(dino_fig), FadeOut(callout_txt), run_time=1.5)
        self.wait(2)