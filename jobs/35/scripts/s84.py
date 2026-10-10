from manim import *
from zenn_rig import *

class S84(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN * 1.4 + LEFT * 3.5,
            playera=PLAYERA_TEAL,
            altura=2.6,
            expresion="pensando",
            pose="de_pie"
        )
        
        self.play(FadeIn(prota, shift=UP))
        
        c = callout(
            "Tu cerebro se adapta a lo que usas.",
            color=TEAL,
            pos=RIGHT * 3.2 + UP * 0.5
        )
        
        f = fuego(pos=RIGHT * 3.5 + DOWN * 1.5, escala=0.9)
        
        self.play(FadeIn(c, shift=LEFT), FadeIn(f))
        
        cambiar_cara(prota, "alegria_pura")
        self.wait(1.5)