from manim import *
from zenn_rig import *

class S48(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        self.play(
            FadeIn(banda_titulo("¡MÁGICA ECOLOGÍA!", color=ORANGE)),
            run_time=0.5
        )
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_VERDE,
            altura=2.4,
            expresion="alegria_pura",
            pose="senalando"
        )
        self.play(FadeIn(prota), run_time=0.8)
        
        pl = planeta(pos=RIGHT*3.5 + UP*0.2, radio=1.2, color=TEAL)
        self.play(FadeIn(pl), run_time=0.8)
        
        c = etiqueta("¡Cuidemos el planeta!", pos=RIGHT*3.5 + UP*2.2, color=INK, font_size=40)
        self.play(FadeIn(c), run_time=0.6)
        
        self.wait(1.3)