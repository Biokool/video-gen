from manim import *
from zenn_rig import *

class S55(Scene):
    def construct(self):
        # Título de pantalla completa (solo uno permitido)
        tc = title_card("EL DÍA QUE NACIÓ EL MITO MODERNO", color=YELLOW)
        self.play(FadeIn(tc))
        self.wait(0.8)
        self.play(FadeOut(tc))
        self.wait(0.4)

        # Protagonista
        prota = protagonista(pos=DOWN*1.2+LEFT*5.5, playera=PLAYERA_NARANJA, altura=2.6, expresion='normal', pose='de_pie')
        self.play(FadeIn(prota))
        self.wait(0.3)
        cambiar_cara(prota, 'sorpresa')
        self.wait(0.3)

        # Pastel
        pastel_obj = pastel(pos=LEFT*4, width=1.8)
        self.play(FadeIn(pastel_obj))
        self.wait(0.5)

        # Idea secundaria usando etiqueta (no title_card ni callout)
        etiqueta_txt = etiqueta(
            "Una ópera cambió nuestra visión del pasado",
            pos=RIGHT*3+UP*1,
            color=ORANGE,
            font_size=40
        )
        self.play(FadeIn(etiqueta_txt))
        self.wait(1.0)

        self.wait(0.2)