from manim import *
from zenn_rig import *

class S79(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        self.play(
            FadeIn(banda_titulo("¿Predisposición vs Habilidad?", color=AZUL_MARINO)),
            FadeIn(caja("Genética", pos=LEFT*3.5 + UP*0.3, width=2.2))
        )
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="pensando",
            pose="de_pie"
        )
        self.play(FadeIn(prota))
        
        flecha = arrow(start=LEFT*1.5 + UP*0.3, end=RIGHT*1.5 + UP*0.3, color=ORANGE, width=8)
        self.play(Create(flecha))
        
        matraz_obj = matraz(pos=RIGHT*3.8 + UP*0.3, escala=1.2, liquido=TEAL)
        self.play(FadeIn(matraz_obj))
        
        self.play(
            FadeIn(etiqueta("¡Habilidad Adquirida!", pos=RIGHT*3.5 + DOWN*1.5, color=ORANGE)),
            run_time=0.8
        )
        
        self.wait(3.2)