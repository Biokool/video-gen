from manim import *
from zenn_rig import *

class S36(Scene):
    def construct(self):
        self.add(fondo(AZUL_MARINO))
        
        titulo = banda_titulo("EL SEGUNDO PICO", color=RED)
        self.play(FadeIn(titulo))
        
        prota = protagonista(pos=DOWN*1.3+LEFT*3.5, playera=PLAYERA_ROJA, altura=2.4, expresion='sorpresa', pose='senalando')
        self.play(FadeIn(prota))
        
        cerebro = planeta(pos=RIGHT*3.2+UP*0.2, radio=1.2, color=TEAL)
        et = etiqueta("¿Tu propio cerebro?", pos=RIGHT*3.2+DOWN*1.3, color=WHITE)
        
        self.play(Create(cerebro), FadeIn(et))
        
        cambiar_cara(prota, 'miedo')
        self.play(
            cerebro.animate.scale(1.1),
            run_time=1.5
        )
        
        et_extra = etiqueta("¡Desconcertante!", pos=RIGHT*3.2+UP*2.2, color=ORANGE)
        self.play(FadeIn(et_extra))
        
        self.wait(1.5)