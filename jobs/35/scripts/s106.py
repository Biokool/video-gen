from manim import *
from zenn_rig import *

class S106(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.5,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="pensando",
            pose="senalando"
        )
        
        self.play(FadeIn(prota))
        
        doc = adn(pos=RIGHT * 3.5 + UP * 0.5, escala=1.2, color=TEAL)
        self.play(Create(doc), run_time=1.5)
        
        c = callout("Estudio Héca 2014\nGenética de lateralidad", color=ORANGE, pos=RIGHT * 3.5 + DOWN * 1.5)
        self.play(FadeIn(c), run_time=1.0)
        
        cambiar_cara(prota, "alegria_pura")
        
        self.wait(6.0)
        
        self.play(FadeOut(prota), FadeOut(doc), FadeOut(c), run_time=1.0)