from manim import *
from zenn_rig import *

class S32(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título único en la zona superior permitida
        self.add(banda_titulo("Especialización en animales", color=TEAL))
        
        # Protagonista con playera verde abajo, a la izquierda, respetando altura y posición
        prota = protagonista(pos=DOWN*1.5+LEFT*4.0, playera=PLAYERA_VERDE, altura=2.4, expresion="sorpresa", pose="senalando")
        self.add(prota)
        
        # Animales estilizados a la derecha usando funciones válidas del rig
        m = gato(pos=RIGHT*1.5+UP*0.5, color='#F2A541', escala=0.8)
        p = pez(pos=RIGHT*3.8+UP*0.5, color=TEAL, escala=0.8)
        d = dino(pos=RIGHT*2.6+DOWN*1.2, color=TEAL, escala=0.8)
        
        self.play(FadeIn(m), FadeIn(p), FadeIn(d), run_time=1.0)
        
        # Animación de transformación/expresión utilizando objetos válidos
        self.play(
            m.animate.shift(UP*0.3),
            run_time=0.8
        )
        
        self.wait(10.2)