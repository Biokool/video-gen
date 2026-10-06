from manim import *
from zenn_rig import *

class S010(Scene):
    def construct(self):
        # Protagonista con playera azul, expresión neutra, posición baja
        prota = protagonista(pos=DOWN*1.2+LEFT*3.0, playera="azul", altura=2.6, expresion="normal", pose="de_pie")
        # Etiqueta con el rango de osmolaridad
        rango_txt = etiqueta("280 - 295 mOsm/kg", (0, 1.5))
        # Barra indicadora simple bajo la etiqueta
        barra = Line(start=LEFT*2, end=RIGHT*2).shift(DOWN*0.5)
        barra.set_stroke(width=8, color=RED)

        # Animaciones
        self.play(FadeIn(prota), run_time=1.5)
        self.play(Write(rango_txt), run_time=1.0)
        self.play(Create(barra), run_time=1.0)
        self.wait(4.0)  # completar ~8 segundos total