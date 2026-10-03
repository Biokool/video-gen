from manim import *
from zenn_rig import *

class S21(Scene):
    def construct(self):
        # Configuración del rig: Fondo de espacio nocturno
        Rig.bg = "space"
        
        # Escena 1: Monigote pensando en el futuro
        self.add(Stickman())
        self.play(RightArrow(0.5))
        self.say("Futuro...", color="PURPLE")
        
        # Llamada a la acción con texto destacado
        self.text_box("Detectores\nGravitacionales", color="TEAL")
        self.play(RightArrow(1.5))