from manim import *
from zenn_rig import *

class S57(Scene):
    def construct(self):
        # protagonista principal
        prota = protagonista(pos=ORIGIN, playera="naranja", altura=3.0,
                             expresion="pensando", pose="de_pie")
        # año destacado
        year_1876 = Text("1876", font_size=48)
        year_1876.next_to(prota, RIGHT, buff=1.5)
        # reloj de pared como segundo props
        clock = reloj_pared(radius=1.0, pos=LEFT*4, hora_3=True)

        self.add(prota, year_1876, clock)
        self.wait(0.5)

        # resaltar el año con rojo
        accent = red_accent(year_1876, scale=1.25)
        self.play(Create(accent))
        self.wait(1)
        self.play(FadeOut(accent))
        self.wait(1)

        # cambiar expresión del protagonista ante la sorpresa
        cambiar_cara(prota, "sorpresa")
        self.wait(1)