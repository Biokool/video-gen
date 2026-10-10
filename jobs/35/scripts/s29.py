from manim import *
from zenn_rig import *

class S29(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.8,
            playera=PLAYERA_VERDE,
            altura=2.4,
            expresion='sorpresa',
            pose='senalando'
        )
        
        self.play(FadeIn(prota), run_time=0.5)
        
        cerebro = adn(pos=RIGHT*3.0 + UP*0.5, escala=1.2, color=TEAL)
        self.play(Create(cerebro), run_time=1.0)
        
        aviso = callout(
            "¡No solo las manos!",
            color=ORANGE,
            pos=RIGHT*3.2 + DOWN*1.5
        )
        self.play(FadeIn(aviso, shift=UP), run_time=0.8)
        
        cambiar_cara(prota, 'euforico')
        
        self.wait(1.2)