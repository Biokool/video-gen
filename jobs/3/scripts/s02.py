from manim import *
# Asumo que zenn_rig.py está disponible y contiene una clase StickFigure.
# Puede que necesites ajustar la ruta de importación de StickFigure según la estructura de tu zenn_rig.
# Por ejemplo, si StickFigure está en zenn_rig/stick_figure.py, sería:
# from zenn_rig.stick_figure import StickFigure
from zenn_rig import StickFigure
import numpy as np

class S02(Scene):
    def construct(self):
        # 1. Crea una figura de palo (stick figure)
        # Posiciona y escala para una mejor visibilidad.
        stick_a = StickFigure().to_edge(LEFT).scale(0.8)
        self.play(Create(stick_a)) # Anima la creación de la figura de palo

        # 2. Crea un objeto objetivo (por ejemplo, un círculo)
        circle = Circle(radius=0.5, color=RED, fill_opacity=0.7).move_to(RIGHT * 3 + UP * 1)
        self.play(Create(circle)) # Anima la creación del círculo

        self.wait(0.5) # Pequeña pausa para ver la configuración inicial

        # --- Animación de "apuntar" personalizada para reemplazar la función stick_point problemática ---

        # 1. Identifica el punto de pivote para la rotación del brazo (el hombro).