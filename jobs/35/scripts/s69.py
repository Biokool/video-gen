from manim import *
from zenn_rig import *

class S69(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=35, color=WHITE))
        
        titulo = banda_titulo("Ventajas Evolutivas", color=YELLOW)
        self.play(
            FadeIn(titulo),
            run_time=1.0
        )
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera=PLAYERA_AZUL, 
            altura=2.6, 
            expresion='sorpresa', 
            pose='senalando'
        )
        self.play(FadeIn(prota), run_time=1.0)
        
        planeta_obj = planeta(pos=RIGHT*2.5 + DOWN*1.5, radio=1.2, color=TEAL)
        self.play(Create(planeta_obj), run_time=1.0)
        
        flecha_asc = arrow(
            start=RIGHT*2.5 + DOWN*0.5, 
            end=RIGHT*2.5 + UP*1.8, 
            color=ORANGE, 
            width=8
        )
        self.play(Create(flecha_asc), run_time=1.5)
        
        d_etiqueta = etiqueta(
            "Corballis, M. C., 2017\nUso de herramientas y comunicación", 
            pos=RIGHT*3.2 + UP*1.0,
            color=YELLOW
        )
        self.play(FadeIn(d_etiqueta), run_time=1.0)
        
        cambiar_cara(prota, 'euforico')
        self.wait(7.0)