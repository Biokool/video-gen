from manim import *
from zenn_rig import *

class S04(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN * 1.3 + LEFT * 4.0, 
            playera=PLAYERA_AZUL, 
            altura=2.4, 
            expresion="sorpresa", 
            pose="senalando"
        )
        
        planeta_tierra = planeta(pos=RIGHT * 3.5 + UP * 0.5, radio=1.2, color=TEAL)
        fuego_boom = fuego(pos=RIGHT * 0.8 + UP * 1.5, escala=1.2)
        
        dato_callout = callout(
            "10% del planeta", 
            color=ORANGE, 
            pos=RIGHT * 3.2 + DOWN * 1.8
        )
        
        self.play(
            FadeIn(prota),
            Create(planeta_tierra),
            FadeIn(fuego_boom),
            run_time=1.0
        )
        
        cambiar_cara(prota, "alegria_pura")
        
        self.play(
            FadeIn(dato_callout),
            run_time=1.0
        )
        
        self.wait(11.0)
        
        self.play(
            FadeOut(prota),
            FadeOut(planeta_tierra),
            FadeOut(fuego_boom),
            FadeOut(dato_callout),
            run_time=1.0
        )