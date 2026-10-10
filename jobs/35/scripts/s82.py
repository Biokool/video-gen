from manim import *
from zenn_rig import *

class S82(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*4 + DOWN*0.2,
                             playera=PLAYERA_NARANJA,
                             altura=2.6,
                             expresion='pensando',
                             pose='de_pie')
        curva_obj = curva(pos=ORIGIN,
                          ancho=5.2,
                          alto=2.8,
                          color=INK,
                          acento=RED)
        callout_obj = callout(text="Conexión neuronal aumenta con movimiento",
                              color=ORANGE,
                              font_size=60,
                              ancho_max=7.0,
                              pos=RIGHT*3.4+UP*1)

        self.play(FadeIn(prota), run_time=2.0)
        self.wait(0.5)
        self.play(Create(curva_obj), run_time=3.0)
        self.wait(0.5)
        self.play(FadeIn(callout_obj), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(red_accent(curva_obj, scale=1.25)), run_time=1.5)
        self.wait(1.0)
        self.play(FadeOut(callout_obj), run_time=0.5)
        self.wait(0.5)