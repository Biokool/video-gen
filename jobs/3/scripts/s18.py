from manim import *
from zenn_rig import *

class S18(Scene):
    def construct(self):
        # VOZ: Hasta la fecha, no hay señales confirmadas. No hemos detectado una sola partícula de materia oscura.
        # Esto ha llevado a algunos físicos a reconsiderar sus modelos, pero la evidencia gravitacional sigue siendo abrumadora.

        # VISUAL: clock_montage
        # Muestra el paso del tiempo y la persistencia en la búsqueda sin éxito.
        self.wait(2) # Pausa inicial para la narración.
        self.play(
            clock_montage(radius=1.6, run_time=10)
        )
        self.wait(3) # Pausa final.