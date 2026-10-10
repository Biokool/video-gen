from manim import *
from zenn_rig import *

class S20(Scene):
    def construct(self):
        self.add(fondo(AZUL_MARINO))
        
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.5,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="pensando",
            pose="senalando"
        )
        
        cerebro = adn(pos=RIGHT * 3.0 + UP * 0.5, escala=1.2, color=TEAL)
        
        signo = etiqueta("?", pos=RIGHT * 3.0 + UP * 2.0, color=YELLOW, font_size=60)
        
        c = callout("¿Cómo funciona?", color=ORANGE, pos=RIGHT * 3.2 + DOWN * 1.2)
        
        self.play(
            FadeIn(prota),
            Create(cerebro),
            FadeIn(signo),
            FadeIn(c),
            run_time=1.5
        )
        
        cambiar_cara(prota, "sorpresa")
        
        self.wait(1.5)