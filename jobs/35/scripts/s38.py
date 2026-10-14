from manim import *
from zenn_rig import *

class S38(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN * 1.3 + LEFT * 3.5,
            playera=PLAYERA_AZUL,
            altura=2.6,
            expresion="confundido",
            pose="de_pie"
        )
        
        self.play(FadeIn(prota), run_time=0.8)
        
        c = matraz(pos=RIGHT * 3.0 + UP * 0.5, escala=1.2, liquido=CORAL)
        self.play(FadeIn(c), run_time=0.8)
        
        call = callout(
            "¿Zurdo o diestro?",
            color=ORANGE,
            pos=RIGHT * 3.2 + UP * 2.0
        )
        self.play(FadeIn(call), run_time=0.8)
        
        cambiar_cara(prota, "pensando")
        self.wait(0.5)
        
        flecha = arrow(
            start=prota.get_top() + RIGHT * 0.5,
            end=c.get_left(),
            color=INK,
            width=6
        )
        self.play(Create(flecha), run_time=0.8)
        
        self.wait(2.5)