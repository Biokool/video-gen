from manim import *
from zenn_rig import *

class S85(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        # Protagonista saludando / feliz abajo a la izquierda
        prota = protagonista(pos=DOWN*1.5 + LEFT*3.8, playera=PLAYERA_NARANJA, altura=2.4, expresion='alegria_pura', pose='senalando')
        self.play(FadeIn(prota, shift=RIGHT), run_time=1.0)
        
        # Callout destacado a la derecha (solo un elemento de texto destacado/título además del protagonista)
        co = callout("¡Nos vemos en la\nsiguiente indagación!", color=TEAL, pos=RIGHT*3.2 + UP*0.5)
        self.play(FadeIn(co, scale=0.8), run_time=1.0)
        
        self.wait(3.0)
        
        self.play(
            FadeOut(prota),
            FadeOut(co),
            run_time=1.0
        )