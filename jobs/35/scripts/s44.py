from manim import *
from zenn_rig import *

class S44(Scene):
    def construct(self):
        banda = banda_titulo("¿Por qué el cielo es azul?", color=YELLOW)
        self.play(FadeIn(banda), run_time=1)
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera="naranja", altura=2.5, expresion="pensando", pose="senalando")
        sol_obj = sol(color=YELLOW, radius=0.7, pos=DOWN*1.2+RIGHT*3.5)
        self.play(FadeIn(prota), Create(sol_obj), run_time=1.5)
        flecha = arrow(start=prota.get_center()+RIGHT*0.5, end=sol_obj.get_center()+LEFT*0.5, color=INK, width=8)
        self.play(Create(flecha), run_time=1)
        self.wait(0.5)