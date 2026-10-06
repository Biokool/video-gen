from manim import *
from zenn_rig import *

class S038(Scene):
    def construct(self):
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_ROJA, altura=2.6, expresion="enojado", pose="de_pie")
        tv = caja(etiqueta="TV", width=1.5).move_to(LEFT*2+UP*0.5)
        movie = pagina_calendario(width=1.7).move_to(RIGHT*2+UP*0.5)
        call = callout(text="Señal entrecortada", color=ORANGE, font_size=96)

        self.play(FadeIn(prota), FadeIn(tv), FadeIn(movie), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(call), run_time=0.6)
        self.wait(2.0)