from manim import *
from zenn_rig import *

class S74(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT * 3.2, playera=PLAYERA_NARANJA, altura=3.0, expresion='pensando', pose='senalando')
        self.play(FadeIn(prota))

        eye = ojo_grande(pos=LEFT * 0.8, escala=1.0, iris=TEAL)
        self.play(FadeIn(eye))

        celula = planeta(pos=RIGHT * 3.2, radio=0.55, color=ORANGE)
        self.play(FadeIn(celula))

        mano = arrow(start=eye.get_right(), end=celula.get_left(), color=INK, width=8)
        self.play(Create(mano), run_time=0.8)

        cambiar_cara(prota, 'sorpresa')
        self.wait(0.8)