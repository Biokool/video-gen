from manim import *
from zenn_rig import *

class S010(Scene):
    def construct(self):
        # personaje principal con playera azul y expresión neutra
        prota = protagonista(ORIGIN, PLAYERA_AZUL, 3.0, 'normal', 'de_pie')
        # etiqueta con el rango de osmolaridad
        rango_label = etiqueta(
            "280 – 295 mOsm/kg",
            pos=RIGHT*3.5+UP*0.5,
            color=INK,
            font_size=40,
            ancho_max=5.5
        )
        # barra indicadora (línea corta) que será resaltada en rojo
        indicador = Line(start=LEFT*0.5, end=RIGHT*0.5).shift(DOWN*1.0)
        indicador.set_color(WHITE)

        self.play(FadeIn(prota), run_time=1.0)
        self.play(FadeIn(rango_label), run_time=1.0)
        self.play(Create(indicador), run_time=1.0)
        self.wait(0.5)
        accent = red_accent(indicador, scale=1.25)
        self.play(Create(accent), run_time=1.0)
        self.wait(2.0)