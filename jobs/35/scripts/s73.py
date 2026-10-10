from manim import *
from zenn_rig import *

class S73(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_AZUL, altura=2.6, expresion='pensando', pose='de_pie')
        
        self.play(
            FadeIn(prota),
            run_time=1.0
        )
        
        etq1 = etiqueta("Cultura", (-1.0, 1.5))
        etq2 = etiqueta("Aprendizaje", (2.0, 1.0))
        
        self.play(
            FadeIn(etq1, shift=UP*0.3),
            FadeIn(etq2, shift=UP*0.3),
            run_time=1.0
        )
        
        cambiar_cara(prota, 'mente_explotada')
        
        dato = callout("Cerebro vs Sentir", color=TEAL, pos=RIGHT*3.6+UP*0.2)
        
        self.play(
            Create(dato),
            run_time=1.0
        )
        
        self.wait(6.5)