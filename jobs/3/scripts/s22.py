from manim import *
from zenn_rig import *

class S22(Scene):
    def construct(self):
        # Monigote para reaccionar a la información
        stick_person = stick_idle(pos=LEFT * 3)

        # Crear la pantalla dividida con los datos
        # La función split_screen espera STRINGS para left_text y right_text,
        # y ella misma crea los objetos Text internos.
        # El objeto 'split' devuelto es un VGroup que contiene los elementos
        # en un orden específico (típicamente [left_text, divider, right_text]).
        split = split_screen("95% MATERIA OSCURA", "100% MATERIA ORDINARIA", divider_color=INK)

        # Escalar el texto DESPUÉS de que split_screen lo haya creado.
        # Accedemos a los objetos Text dentro del VGroup 'split' por su índice.
        # Asumiendo que el texto izquierdo es el primer elemento y el derecho el tercero.
        split[0].scale(0.7) # Texto izquierdo
        split[2].scale(0.7) # Texto derecho

        # Animaciones
        self.play(
            FadeIn(stick_person),
            run_time=1
        )
        self.play(
            Create(split),
            run_time=3
        )

        # Añadir expresión de sorpresa al monigote
        exp = expresion(stick_person, 'sorpresa')
        self.play(
            FadeIn(exp),
            run_time=0.5
        )

        # Resaltar la parte de la materia oscura
        # Accedemos al objeto Text izquierdo por su índice.
        accent_dark = red_accent(split[0])
        self.play(
            FadeIn(accent_dark),
            run_time=0.5
        )
        self.wait(2) # Pausa para la narración: "tú eres 95% materia oscura en términos de masa cósmica"

        # Cambiar el resalte a la materia ordinaria
        # Accedemos al objeto Text derecho por su índice.
        accent_ordinary = red_accent(split[2])
        self.play(
            FadeOut(accent_dark),
            FadeIn(accent_ordinary),
            run_time=1
        )
        self.wait(2) # Pausa para la narración: "pero biológicamente eres 100% materia ordinaria."

        # Limpiar la escena
        self.play(
            FadeOut(accent_ordinary),
            FadeOut(exp),
            FadeOut(stick_person),
            FadeOut(split),
            run_time=1
        )
        self.wait(1)