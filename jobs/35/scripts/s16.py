from manim import *
from zenn_rig import *

class S16(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera=PLAYERA_ROJA, 
            altura=2.6, 
            expresion='sorpresa', 
            pose='senalando'
        )
        
        cerebro = planeta(pos=RIGHT*3.0 + UP*0.5, radio=1.2, color=CORAL)
        etq = etiqueta("Hemisferio izq/der", (3.0, -1.2))
        
        msg = callout("¡Sorpresa en el hemisferio derecho!", color=ORANGE, pos=RIGHT*3.0 + UP*2.2)
        
        self.play(
            FadeIn(prota),
            FadeIn(cerebro),
            FadeIn(etq),
            FadeIn(msg),
            run_time=1.5
        )
        
        cambiar_cara(prota, 'alegria_pura')
        self.wait(5.5)