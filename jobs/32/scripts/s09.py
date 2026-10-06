from manim import *
from zenn_rig import *

class S09(Scene):
    def construct(self):
        # protagonista con playera azul y expresión de sorpresa (alerta)
        prota = protagonista(pos=ORIGIN, playera="azul", altura=3.0, expresion="sorpresa", pose="de_pie")
        self.play(FadeIn(prota), run_time=1.0)
        self.wait(0.5)

        # gota de sangre (pequeño círculo rojo)
        drop = Dot(radius=0.15, color=RED).move_to(prota.get_center() + DOWN*0.5 + RIGHT*0.5)
        self.play(Create(drop), run_time=0.8)
        self.wait(0.4)

        # etiqueta de osmolaridad subiendo
        label = etiqueta("Osmolaridad plasmática subiendo", (0, 2.2))
        self.play(Write(label), run_time=1.0)
        self.wait(1.2)

        # leve movimiento de la gota para indicar ascenso
        self.play(drop.animate.shift(UP*0.4), run_time=0.8)
        self.wait(1.0)  # total ~9 segundos