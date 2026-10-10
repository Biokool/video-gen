from manim import *
from zenn_rig import *

class S72(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título superior seguro (usar add en lugar de play con banda_titulo si devuelve un Mobject estático)
        bt = banda_titulo("¡TU CEREBRO TE MIENTE!", color=RED)
        self.add(bt)
        
        # Protagonista abajo a la izquierda (camiseta roja, asombro)
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_ROJA,
            altura=2.6,
            expresion='sorpresa',
            pose='senalando'
        )
        self.play(FadeIn(prota))
        
        # Cerebro / Matraz estilizado con ojo grande a la derecha
        cerebro = matraz(pos=RIGHT*3.5 + UP*0.2, escala=1.3, liquido=RED)
        ojo = ojo_grande(pos=RIGHT*3.5 + UP*1.4, escala=0.7, iris=RED)
        
        self.play(FadeIn(cerebro), FadeIn(ojo))
        
        # Uso de etiqueta() en lugar de callout para evitar duplicidad de elementos destacados pesados
        et = etiqueta("¡Mano dominante falsa!", pos=RIGHT*3.5 + DOWN*1.5, color=ORANGE, font_size=40)
        self.play(FadeIn(et))
        
        self.wait(3.0)