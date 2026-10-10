from manim import *
from zenn_rig import *

class S86(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.2,
            playera=PLAYERA_NARANJA,
            altura=2.5,
            expresion="euforico",
            pose="senalando"
        )
        
        caja_sus = caja("SUSCRÍBETE", pos=RIGHT * 2.5 + UP * 0.5, width=3.2)
        
        call = callout(
            "¡No te pierdas ninguna respuesta!",
            color=ORANGE,
            pos=RIGHT * 2.8 + DOWN * 1.5
        )
        
        self.play(
            FadeIn(prota, shift=UP),
            Create(caja_sus),
            run_time=1.0
        )
        
        self.play(
            FadeIn(call, shift=LEFT),
            run_time=1.0
        )
        
        self.wait(5.0)