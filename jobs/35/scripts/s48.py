from manim import *
from zenn_rig import *

class S48(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.2,
            playera=AZUL_MARINO,
            altura=2.6,
            expresion="alegria_pura",
            pose="senalando"
        )
        
        c = callout(
            "¡Suscríbete!",
            color=ORANGE,
            pos=RIGHT*3.0 + UP*0.5
        )
        
        b = caja(
            etiqueta="EL PORQUÉ",
            pos=RIGHT*3.0 + DOWN*1.0,
            width=3.2
        )
        
        self.play(FadeIn(prota), FadeIn(c), Create(b), run_time=1.5)
        cambiar_cara(prota, "feliz")
        self.wait(4.5)