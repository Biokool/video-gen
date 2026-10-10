from manim import *
from zenn_rig import *

class S17(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.8,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="pensando",
            pose="de_pie"
        )
        
        self.play(FadeIn(prota), run_time=0.8)
        
        t = banda_titulo("El entorno prenatal y el desarrollo", color=AZUL_MARINO)
        self.add(t)
        
        m = matraz(pos=RIGHT*3.0 + DOWN*0.2, escala=1.2, liquido=TEAL)
        a = adn(pos=RIGHT*3.0 + UP*1.6, escala=0.8, color=TEAL)
        
        self.play(Create(m), FadeIn(a), run_time=1.0)
        
        c = etiqueta("Ambiente intrauterino crucial", pos=RIGHT*3.2+UP*0.8, color=ORANGE)
        self.play(FadeIn(c), run_time=0.8)
        
        self.wait(2.6)