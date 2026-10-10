from manim import *
from zenn_rig import *

class S68(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=30, seed=42, color=WHITE))
        
        self.add(banda_titulo("EVOLUCIÓN Y ASIMETRÍA", color=ORANGE))
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*4.0,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="mente_explotada",
            pose="senalando"
        )
        
        p = planeta(pos=RIGHT*4.0 + UP*1.0, radio=1.2, color=TEAL)
        d = dino(pos=RIGHT*2.0 + DOWN*1.5, color=TEAL, escala=1.1)
        
        flecha = arrow(start=LEFT*2.0 + DOWN*1.0, end=RIGHT*1.0 + DOWN*1.5, color=WHITE, width=6)
        
        et = etiqueta("Especialización animal", pos=RIGHT*3.5 + DOWN*0.8, color=WHITE, font_size=40)
        
        self.play(
            FadeIn(p),
            FadeIn(d),
            Create(flecha),
            FadeIn(et),
            run_time=1.5
        )
        
        cambiar_cara(prota, "feliz")
        
        self.wait(10.0)