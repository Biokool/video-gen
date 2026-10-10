from manim import *
from zenn_rig import *

class S65(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        # Una sola llamada de título (banda_titulo es la única barra superior permitida)
        b_tit = banda_titulo(
            texto="Pero aquí viene otro giro: el azar",
            color=ORANGE
        )
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="sorpresa",
            pose="senalando"
        )
        
        dado = caja(etiqueta="AZAR", pos=RIGHT*3.0 + UP*0.5, width=2.0)
        
        # Se elimina el callout duplicado para cumplir estrictamente con la regla
        # de no tener múltiples elementos de texto superpuestos.
        
        self.play(
            FadeIn(b_tit),
            FadeIn(prota),
            Create(dado),
            run_time=1.0
        )
        
        self.play(
            dado.animate.rotate(0.5).shift(UP*0.3),
            run_time=1.5
        )
        
        self.wait(9.5)