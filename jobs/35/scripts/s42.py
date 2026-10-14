from manim import *
from zenn_rig import *

class S42(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.5,
            playera=PLAYERA_MORADA,
            altura=2.4,
            expresion="pensando",
            pose="de_pie"
        )
        
        caja_piano = caja("PIANO", pos=RIGHT * 2.5 + DOWN * 0.5, width=3.2)
        
        self.play(
            FadeIn(prota),
            Create(caja_piano),
            run_time=1.0
        )
        
        cambiar_cara(prota, "alegria_pura")
        self.wait(0.5)
        
        callout_texto = callout(
            "Simetría bilateral en el cerebro",
            color=CORAL,
            pos=RIGHT * 3.0 + UP * 1.2
        )
        
        self.play(
            FadeIn(callout_texto),
            run_time=1.0
        )
        
        self.wait(5.0)
        
        self.play(
            FadeOut(prota),
            FadeOut(caja_piano),
            FadeOut(callout_texto),
            run_time=1.0
        )