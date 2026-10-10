from manim import *
from zenn_rig import *

class S41(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="sorpresa",
            pose="senalando"
        )
        
        self.play(FadeIn(prota))
        
        self.play(
            FadeIn(
                callout(
                    "¡Increíble descubrimiento!",
                    color=ORANGE,
                    pos=RIGHT*3.2 + UP*1.0
                )
            ),
            run_time=1.0
        )
        
        diamante = moneda_dorada(texto="★", pos=RIGHT*3.2 + DOWN*1.0, radio=0.9)
        self.play(Create(diamante), run_time=1.0)
        
        cambiar_cara(prota, "alegria_pura")
        
        self.wait(1.5)