from manim import *
from zenn_rig import *

class S11(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT * 3.2 + DOWN * 0.9, playera='azul',
                             altura=2.8, expresion='pensando', pose='senalando')
        corona = moneda_dorada(texto='★', pos=LEFT * 3.2 + UP * 2.3, radio=0.55)
        ojo = ojo_grande(pos=RIGHT * 2.8 + DOWN * 0.6, escala=1.2, iris=TEAL)
        co = callout('¡MAESTRO!', color=ORANGE, font_size=72)
        co.move_to(RIGHT * 2.5 + UP * 2.7)
        flecha = arrow(start=LEFT * 1.9 + UP * 0.1,
                       end=RIGHT * 1.4 + DOWN * 0.6, color=INK, width=6)

        self.play(FadeIn(prota), run_time=0.6)
        self.play(FadeIn(ojo), GrowFromCenter(corona), run_time=0.6)
        self.play(FadeIn(co), run_time=0.5)
        cambiar_cara(prota, 'euforico')
        self.play(Create(flecha), corona.animate.shift(UP * 0.12), run_time=0.6)
        self.wait(1.0)