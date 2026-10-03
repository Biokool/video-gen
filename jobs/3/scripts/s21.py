from manim import *
from zenn_rig import *

class S21(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(15))
        
        # Elementos visuales
        mono = stick_idle(ORIGIN, color=WHITE)
        self.add(mono)
        
        telescopio = planeta(ORIGIN + LEFT*3 + UP*1, 0.5, TEAL)
        detector = caja("LIGO", ORIGIN + RIGHT*3 + DOWN*0.5)
        
        # Animaciones
        self.play(FadeIn(mono, shift=UP*0.5), run_time=1.0)
        self.play(FadeIn(telescopio, shift=RIGHT*0.5), FadeIn(detector, shift=LEFT*0.5), run_time=1.0)
        
        # Expresión de esperanza/futuro
        self.play(expresion(mono, "feliz"), run_time=0.5)
        
        # Señalar al telescopio usando stick_point
        self.play(stick_point(mono, telescopio), run_time=1.0)
        
        # Callout
        call = callout("Nuevo Futuro", color=YELLOW)
        self.play(FadeIn(call, shift=DOWN*0.5), run_time=0.5)
        
        self.wait(1.5)