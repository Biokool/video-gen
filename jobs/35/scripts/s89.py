from manim import *
from zenn_rig import *

class S89(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = version_prota(5, pos=DOWN*1.2+LEFT*3.5)
        cambiar_cara(prota, 'pensando')
        
        cerebro_adn = adn(pos=RIGHT*3.0+UP*0.5, escala=1.2, color=TEAL)
        
        self.play(
            FadeIn(prota),
            Create(cerebro_adn),
            run_time=1.0
        )
        
        c = callout("¡Aleatoriedad!", color=ORANGE, pos=RIGHT*3.2+DOWN*1.5)
        
        self.play(
            FadeIn(c),
            run_time=1.0
        )
        
        prota.animate.shift(RIGHT * 2.0)
        self.play(
            prota.animate.shift(RIGHT * 2.0),
            run_time=2.0
        )
        
        cambiar_cara(prota, 'sorpresa')
        
        self.wait(3.0)