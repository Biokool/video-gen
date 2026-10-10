from manim import *
from zenn_rig import *

class S57(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN * 1.3 + LEFT * 3.5,
            playera=PLAYERA_NARANJA,
            altura=2.4,
            expresion='sorpresa',
            pose='senalando'
        )
        
        self.play(FadeIn(prota), run_time=0.5)
        
        c = caja(etiqueta="¡WOW!", pos=RIGHT * 3.0 + UP * 0.5, width=2.0)
        self.play(Create(c), run_time=0.8)
        
        cot = callout(text="¡Datos asombrosos!", color=ORANGE, pos=RIGHT * 2.8 + UP * 2.1)
        self.play(FadeIn(cot), run_time=0.5)
        
        cambiar_cara(prota, 'alegria_pura')
        self.wait(1.9)