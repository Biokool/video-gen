from manim import *
from zenn_rig import *

class S09(Scene):
    def construct(self):
        # Protagonista azul, pensando
        prota = protagonista(pos=LEFT*3 + DOWN*0.5, playera="azul", altura=2.6,
                             expresion="pensando", pose="de_pie")
        # Cama representada por una caja etiquetada
        bed = caja(etiqueta="cama", pos=RIGHT*3 + DOWN*0.5, width=1.5)
        # Bucle azul alrededor de la cama
        loop = sol(color=BLUE, radius=1.2, pos=bed.get_center())
        # Callout corto con signo de interrogación
        q = callout(text="¿?", color=ORANGE, font_size=96)

        self.play(FadeIn(prota), FadeIn(bed), run_time=0.8)
        self.play(Create(loop), run_time=0.8)
        self.play(FadeIn(q), run_time=0.8)
        self.wait(2)