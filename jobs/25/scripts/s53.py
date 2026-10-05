from manim import *
from zenn_rig import *

class S53(Scene):
    def construct(self):
        bg = fondo(INK)
        self.add(bg)

        luz = sol(color=WHITE, radius=1.8, pos=RIGHT * 2.5)
        self.play(FadeIn(luz, run_time=1.0))

        ojo = ojo_grande(pos=RIGHT * 2.5, escala=1.0, iris=YELLOW)
        self.play(FadeIn(ojo, run_time=1.0))

        prota = protagonista(pos=LEFT * 4.5, playera='amarilla', expresion='pensando', pose='de_pie')
        self.play(FadeIn(prota, run_time=0.5))
        self.play(prota.animate.shift(RIGHT * 1.5), run_time=1.2)

        rotulo = callout("SIN LUZ, NO VEMOS", color=YELLOW)
        rotulo.to_edge(UP)
        self.play(FadeIn(rotulo, run_time=0.8))
        self.wait(1.0)