from manim import *
from zenn_rig import *

class S12(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título único en la banda superior (zona segura superior) - usando Write en lugar de FadeIn/animación directa de mobject si genera conflicto
        bt = banda_titulo("Hemisferios Cerebrales", color=AZUL_MARINO)
        self.play(FadeIn(bt))
        
        # Protagonista abajo a la izquierda (respetando la banda superior y zona y<=-1.2)
        prota = protagonista(pos=DOWN*1.5 + LEFT*3.5, playera=PLAYERA_AZUL, altura=2.4, expresion='mente_explotada', pose='senalando')
        self.play(FadeIn(prota))
        
        # Props visuales representativos en el lado derecho
        cerebro_izq = planeta(pos=RIGHT*2.5 + UP*0.5, radio=1.0, color=TEAL)
        cerebro_der = planeta(pos=RIGHT*4.8 + UP*0.5, radio=1.0, color=RED)
        
        etiqueta_izq = etiqueta("Izquierdo", pos=RIGHT*2.5 + DOWN*0.8)
        etiqueta_der = etiqueta("Derecho", pos=RIGHT*4.8 + DOWN*0.8)
        
        flecha_cerebro = arrow(start=RIGHT*3.5 + UP*0.5, end=RIGHT*3.8 + UP*0.5, color=INK)
        
        self.play(
            FadeIn(cerebro_izq),
            FadeIn(cerebro_der),
            FadeIn(flecha_cerebro),
            FadeIn(etiqueta_izq),
            FadeIn(etiqueta_der),
            run_time=1.5
        )
        
        self.wait(8.0)