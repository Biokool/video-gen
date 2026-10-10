from manim import *
from zenn_rig import *

class S66(Scene):
    def construct(self):
        self.add(fondo(AZUL_MARINO))
        
        titulo = banda_titulo("Aleatoriedad y Neuronas", color=ORANGE)
        self.play(
            FadeIn(titulo),
            run_time=0.8
        )
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*3.8,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="mente_explotada",
            pose="senalando"
        )
        self.play(FadeIn(prota), run_time=0.6)
        
        d = digitos(pos=RIGHT*3.0 + UP*0.5, size=1.2)
        c = curva(pos=RIGHT*3.0 + DOWN*1.2, ancho=4.5, alto=2.2, color=TEAL, acento=CORAL)
        self.play(Create(d), Create(c), run_time=1.2)
        
        msg = etiqueta("¡Factor decisivo!", pos=RIGHT*3.2+UP*1.9, color=YELLOW)
        self.play(FadeIn(msg), run_time=0.6)
        
        cambiar_cara(prota, "feliz")
        
        self.wait(2.5)