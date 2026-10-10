from manim import *
from zenn_rig import *

class S67(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_AZUL,
            altura=2.5,
            expresion="pensando",
            pose="de_pie"
        )
        self.add(prota)
        
        moneda = moneda_dorada(texto="$", pos=RIGHT*2.5 + UP*0.5, radio=1.2)
        self.play(FadeIn(moneda, shift=UP))
        
        flecha = arrow(start=RIGHT*2.5 + UP*2.2, end=RIGHT*2.5 + UP*0.9)
        self.play(Create(flecha))
        
        c = callout(text="¡Azar puro!", color=ORANGE, pos=RIGHT*3.2 + DOWN*1.5)
        self.play(FadeIn(c, shift=LEFT))
        
        cambiar_cara(prota, "sorpresa")
        
        self.wait(5.0)