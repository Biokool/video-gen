from manim import *
from zenn_rig import *

class S92(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        self.play(
            FadeIn(banda_titulo("¿ES TU CEREBRO MINTIENDO?", color=ORANGE)),
            FadeIn(caja("CEREBRO", pos=UP*0.5 + LEFT*3.5, width=2.2))
        )
        
        prota = protagonista(
            pos=DOWN*1.2 + RIGHT*3.0,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="mente_explotada",
            pose="senalando"
        )
        self.play(FadeIn(prota))
        
        c = etiqueta("¡Tu cerebro miente sobre tu mano!", pos=LEFT*2.2 + UP*0.2, color=RED, font_size=36)
        self.play(FadeIn(c))
        
        self.wait(1.5)
        
        cambiar_cara(prota, "confundido")
        self.play(
            prota.animate.shift(LEFT*0.5),
            run_time=1.0
        )
        
        self.wait(2.0)