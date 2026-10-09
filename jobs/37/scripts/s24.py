from manim import *
from zenn_rig import *

class S24(Scene):
    def construct(self):
        title = banda_titulo("El origen del casco vikingo", color=ORANGE)
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_AZUL, altura=2.5, expresion='pensando', pose='de_pie')
        artista = stick_idle(pos=RIGHT*2.5+UP*0.5, height=2.2, color=INK)
        expresion(artista, 'normal')
        casco = casco_vikingo(pos=RIGHT*2.5+UP*2.0, escala=1.0)
        programa = caja(etiqueta="Programa 1876", pos=LEFT*2.5+UP*0.5)

        self.play(FadeIn(title), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(prota), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(artista), FadeIn(casco), FadeIn(programa), run_time=1)
        self.wait(0.5)
        pointer = arrow(artista.get_center(), casco.get_center(), color=INK, width=8)
        self.play(Create(pointer), run_time=1)
        self.wait(1.0)
        self.play(FadeOut(title), FadeOut(prota), FadeOut(artista), FadeOut(casco), FadeOut(programa), run_time=1)
        self.wait(1.0)