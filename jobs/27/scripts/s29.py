from manim import *
from zenn_rig import *

class S29(Scene):
    def construct(self):
        self.add(fondo_papel())
        prota = protagonista(DOWN*1.2+LEFT*3.5, PLAYERA_AMARILLA, altura=2.6,
                             expresion='pensando', pose='de_pie')
        self.play(FadeIn(prota), run_time=0.8)

        lap = lapida('Geocentrismo', pos=LEFT*0.4+DOWN*1.4, ancho=2.4)
        rel = reloj_pared(radius=0.9, pos=RIGHT*3.6+DOWN*0.9)
        self.play(FadeIn(lap, shift=UP*0.4), FadeIn(rel, shift=DOWN*0.4), run_time=0.9)

        co = callout('Mil años de teoría equivocada', color=YELLOW,
                     pos=RIGHT*3.4+UP*1.7)
        self.play(FadeIn(co, shift=LEFT*0.3), run_time=0.8)

        acento = red_accent(lap)
        self.play(FadeIn(acento, scale=0.8), run_time=0.8)

        cambiar_cara(prota, 'triste')
        self.wait(0.6)

        self.play(Indicate(rel, color=RED), run_time=0.8)
        self.wait(0.5)