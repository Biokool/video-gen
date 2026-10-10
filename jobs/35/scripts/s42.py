from manim import *
from zenn_rig import *

class S42(Scene):
    def construct(self):
        # Banda de título (única)
        banda = titulo_seguro("El Porqué", color=INK)
        self.add(banda)

        # Protagonista abajo a la izquierda
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_NARANJA,
            altura=2.5,
            expresion="feliz",
            pose="de_pie"
        )
        # Prop: sol a la derecha
        sol_obj = sol(color=YELLOW, radius=0.7, pos=RIGHT*2.5 + UP*0.5)

        self.play(FadeIn(prota), FadeIn(sol_obj), run_time=1.0)
        self.wait(1.2)
        self.play(prota.animate.shift(RIGHT*0.3), run_time=0.5)
        self.wait(0.8)