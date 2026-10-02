from manim import *
from zenn_rig import *

class S05(Scene):
    def construct(self):
        # Fondo blanco por defecto, no es necesario especificar.

        # 1. Crear el agujero negro (representado por un círculo oscuro)
        # y el monigote inicial.
        black_hole = Circle(radius=1.5, color=INK, fill_opacity=1).move_to(RIGHT * 2)
        zenn = stick_idle(pos=LEFT * 4) # Monigote a la izquierda

        self.play(
            Create(black_hole),
            FadeIn(zenn)
        )
        self.wait(1)

        # 2. Definir el estado final del monigote: una línea muy fina y estirada
        # que se extiende desde la posición inicial del monigote hasta el interior del agujero negro.
        # La línea se centrará verticalmente con la posición inicial del monigote.
        final_stretched_line = Line(
            start=LEFT * 4.5, # Un poco más a la izquierda que la posición inicial del monigote para enfatizar el estiramiento
            end=RIGHT * 3,    # Extendiéndose profundamente en el agujero negro
            stroke_width=1,   # Muy delgado para simular "hebra de átomos"
            color=INK
        )
        # Aseguramos que la línea esté alineada verticalmente con el centro del monigote original
        final_stretched_line.set_y(zenn.get_y())

        # 3. Animar la transformación del monigote en la línea estirada.
        # Esta animación moverá el monigote hacia el agujero negro mientras se deforma progresivamente.
        self.play(
            Transform(zenn, final_stretched_line),
            run_time=18, # Duración larga para un efecto gradual
            rate_func=linear # Velocidad constante para la progresión
        )
        self.wait(3) # Esperar un momento al final para mostrar el resultado.