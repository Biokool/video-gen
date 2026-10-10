from manim import *
from zenn_rig import *

class S58(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        self.play(
            FadeIn(banda_titulo("EL SECRETO DE LAS ESTRELLAS", color=AZUL_MARINO)),
            run_time=0.5
        )
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*4.0,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="mente_explotada",
            pose="senalando"
        )
        self.play(FadeIn(prota), run_time=0.8)
        
        planeta_obj = planeta(pos=RIGHT*3.5 + UP*0.2, radio=1.2, color=TEAL)
        self.play(Create(planeta_obj), run_time=0.8)
        
        c = etiqueta("¡Todo está conectado!", pos=RIGHT*3.5 + DOWN*1.5, color=ORANGE, font_size=40)
        self.play(FadeIn(c), run_time=0.8)
        
        self.wait(1.1)