from manim import *
from zenn_rig import *

class S73(MovingCameraScene):
    def construct(self):
        # Fondo oscuro para simular mundo microscópico
        self.add(fondo(INK))
        estrellas_moleculas = estrellas(n=42, seed=7, color=WHITE)
        self.add(estrellas_moleculas)

        # Protagonista con playera naranja, expresión de asombro
        por = protagonista(
            pos=LEFT * 3.2 + DOWN * 0.3,
            playera=PLAYERA_NARANJA,
            altura=3.0,
            expresion="sorpresa",
            pose="de_pie",
        )
        # Ojo que representa el zoom / visión cercana
        ojo = ojo_grande(pos=RIGHT * 3.2 + UP * 0.8, escala=0.9, iris=TEAL)

        self.play(FadeIn(por, shift=UP * 0.4), Create(ojo))
        self.wait(0.3)

        # El porqué señala con sorpresa; el ojo se acerca al centro
        self.play(por.animate.shift(LEFT * 0.4), run_time=0.5)
        self.play(
            ojo.animate.scale(1.8).shift(LEFT * 2.0),
            por.animate.scale(0.9),
            run_time=1.2,
        )
        self.wait(0.3)

        # Zoom extremo de cámara hacia el ojo / materia visible
        self.play(
            self.camera.frame.animate.scale(0.25).move_to(ojo.get_center()),
            run_time=2.0,
        )
        self.wait(0.6)