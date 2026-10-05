from manim import *
import numpy as np
from zenn_rig import *

class S18(Scene):
    def construct(self):
        def _p(a):
            if a is None:
                return
            if isinstance(a, Animation):
                self.play(a)
            elif isinstance(a, (list, tuple)):
                anims = [x for x in a if isinstance(x, Animation)]
                if anims:
                    self.play(*anims)

        prota = protagonista(pos=np.array([-5.0, -0.7, 0.0]), playera="verde", altura=2.7,
                             expresion='feliz', pose='senalando')
        ojo = ojo_grande(pos=np.array([5.9, 1.5, 0.0]), escala=0.7)
        a = stick_idle(pos=np.array([-1.2, -1.0, 0.0]), height=1.9)
        b = stick_idle(pos=np.array([1.4, -1.0, 0.0]), height=1.9)

        self.play(FadeIn(prota, shift=RIGHT * 0.4), FadeIn(ojo), run_time=0.7)
        self.play(FadeIn(a), FadeIn(b), run_time=0.4)

        _p(stick_point(a, b.get_center() + UP * 0.9))
        _p(stick_walk(b, b.get_center() + RIGHT * 0.6, run_time=1.0, steps=4))

        self.play(FadeIn(etiqueta("personas y herramientas", np.array([1.3, 0.75, 0.0]),
                                  color=INK, font_size=36)), run_time=0.4)
        self.play(FadeIn(callout("Interactuo", color=ORANGE)), run_time=0.5)

        _p(cambiar_cara(prota, 'alegria_pura'))
        self.wait(0.3)