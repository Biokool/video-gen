from manim import *
from zenn_rig import *

class S30(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN * 1.3 + LEFT * 3.5,
            playera=PLAYERA_AMARILLA,
            altura=2.5,
            expresion='sorpresa',
            pose='de_pie'
        )
        
        moneda = moneda_dorada(texto='?', pos=UP * 0.5 + RIGHT * 2.5, radio=1.2)
        
        c = callout(
            "¡Pura casualidad!",
            color=ORANGE,
            pos=RIGHT * 3.4 + UP * 1.0
        )
        
        self.play(
            FadeIn(prota, shift=UP),
            FadeIn(moneda, shift=DOWN),
            FadeIn(c, shift=RIGHT),
            run_time=1.0
        )
        
        self.play(
            moneda.animate.rotate(2 * PI),
            run_time=3.0,
            rate_func=linear
        )
        
        cambiar_cara(prota, 'mente_explotada')
        
        self.wait(2.0)