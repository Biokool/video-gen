from manim import *
from zenn_rig import *

class S042(Scene):
    def construct(self):
        prota = protagonista(
            pos=UP*0.5+LEFT*3.5,
            playera=PLAYERA_AMARILLA,
            altura=2.2,
            expresion='decidido',
            pose='de_pie'
        )
        celda = stick_idle(pos=DOWN*0.5+RIGHT*2.0, height=1.0, color=TEAL)
        expresion(celda, 'normal')
        sangre = caja("Sangre", pos=DOWN*1.5, width=3.0)

        self.play(FadeIn(prota), FadeIn(celda), FadeIn(sangre), run_time=1.5)
        self.wait(0.5)

        arr = arrow(celda.get_center(), sangre.get_center())
        self.play(Create(arr), run_time=1.0)
        self.wait(0.4)

        cambiar_cara(prota, 'feliz')
        self.wait(0.8)

        self.play(prota.animate.shift(UP*0.1), run_time=0.2)
        self.play(prota.animate.shift(DOWN*0.1), run_time=0.2)
        self.wait(0.5)