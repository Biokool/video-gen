from manim import *
from zenn_rig import *

class S47(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=12, seed=7, color=WHITE))

        prota = protagonista(
            pos=LEFT * 3.5,
            playera="amarilla",
            altura=3.0,
            expresion="pensando",
            pose="senalando"
        )
        ojo = ojo_grande(pos=RIGHT * 3.5, escala=1.1, iris=YELLOW)
        punto = Dot(ORIGIN, radius=0.12, color=YELLOW)

        self.play(FadeIn(prota), FadeIn(ojo), run_time=0.5)
        self.play(Create(punto), run_time=0.4)

        cambiar_cara(prota, "sorpresa")
        self.play(punto.animate.scale(1.4), run_time=0.5)
        self.wait(0.6)