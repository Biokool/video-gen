from manim import *
from zenn_rig import *

class S46(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=30, color=WHITE))
        
        self.add(banda_titulo("TU CEREBRO SE ADAPTA A LO QUE USAS", color=TEAL))
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_TEAL,
            altura=2.6,
            expresion='mente_explotada',
            pose='senalando'
        )
        self.add(prota)
        
        cerebro_adn = adn(pos=RIGHT*3.2 + UP*0.2, escala=1.2, color=TEAL)
        self.add(cerebro_adn)
        
        arr = arrow(start=LEFT*1.8 + UP*0.2, end=RIGHT*1.8 + UP*0.2, color=WHITE, width=6)
        self.add(arr)
        
        self.play(
            FadeIn(cerebro_adn),
            Create(arr),
            run_time=1.5
        )
        
        cambiar_cara(prota, 'alegria_pura')
        
        self.wait(5.5)