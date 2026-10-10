from manim import *
from zenn_rig import *

class S27(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_VERDE, altura=2.6, expresion='confundido', pose='de_pie')
        
        cerebro = adn(pos=RIGHT*3.0+UP*0.5, escala=1.2, color=TEAL)
        
        self.play(
            FadeIn(prota, shift=UP),
            Create(cerebro),
            run_time=1.5
        )
        
        cambiar_cara(prota, 'sorpresa')
        self.wait(0.5)
        
        c = callout("¡Dominancia cruzada!", color=ORANGE, pos=RIGHT*3.2+DOWN*1.5)
        self.play(FadeIn(c), run_time=1.0)
        
        self.wait(3.0)
        
        self.play(
            FadeOut(prota),
            FadeOut(cerebro),
            FadeOut(c),
            run_time=1.0
        )