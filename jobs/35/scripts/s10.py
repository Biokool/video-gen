from manim import *
from zenn_rig import *

class S10(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        self.play(
            FadeIn(banda_titulo("LATERALIDAD Y CIENCIA", color=AZUL_MARINO)),
            run_time=1.0
        )
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*3.8,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="pensando",
            pose="de_pie"
        )
        self.play(FadeIn(prota), run_time=1.0)
        
        g = grafica_barras(
            pos=RIGHT*3.0 + UP*0.2,
            valores=(90, 10, 50, 75),
            ancho=4.0,
            color=TEAL
        )
        self.play(Create(g), run_time=1.5)
        
        c = etiqueta("¡No es moda!", pos=RIGHT*3.5+UP*2.2, color=ORANGE, font_size=40)
        self.play(FadeIn(c), run_time=1.0)
        
        cambiar_cara(prota, "alegria_pura")
        
        self.wait(2.5)