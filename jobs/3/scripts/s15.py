from manim import *
from zenn_rig import *

class S15(Scene):
    def construct(self):
        self.add(fondo(INK))
        estrellas_obj = estrellas(15)
        self.add(estrellas_obj)
        
        astronauta = stick_idle(LEFT * 3.5, color=WHITE)
        self.add(astronauta)
        
        galaxy = planeta(ORIGIN, 1.5, TEAL)
        self.play(FadeIn(galaxy), run_time=2)
        
        self.play(
            Transform(galaxy, planeta(ORIGIN, 1.2, YELLOW)),
            run_time=2.5
        )
        
        self.play(
            astronauta.animate.move_to(LEFT * 1.5),
            run_time=1.5
        )
        
        self.play(
            stick_think(astronauta, "¿Masa invisible?"),
            run_time=2
        )
        
        self.play(
            Transform(galaxy, planeta(ORIGIN, 1.8, ORANGE)),
            run_time=2.5
        )
        
        self.play(
            FadeOut(galaxy),
            run_time=1.5
        )
        
        self.play(
            FadeOut(astronauta),
            FadeOut(estrellas_obj),
            run_time=1.5
        )