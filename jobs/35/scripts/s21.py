from manim import *
from zenn_rig import *

class S21(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        # Banda de título superior (ÚNICA llamada de título en la escena)
        self.play(Write(banda_titulo("LOS DOS HEMISFERIOS", color=TEAL)))
        
        # Protagonista abajo a la izquierda (evitando zona de banda y subtítulos)
        prota = protagonista(pos=DOWN*1.3+LEFT*3.8, playera=PLAYERA_VERDE, altura=2.4, expresion="pensando", pose="de_pie")
        self.play(FadeIn(prota))
        
        # Dos cerebros o un split/curva que representa la división hemisférica
        cerebro_izq = matraz(pos=LEFT*0.8+UP*0.2, escala=1.1, liquido=CORAL)
        cerebro_der = matraz(pos=RIGHT*1.8+UP*0.2, escala=1.1, liquido=AZUL_MARINO)
        
        etq_izq = etiqueta("Izquierdo", (-0.8, -1.0))
        etq_der = etiqueta("Derecho", (1.8, -1.0))
        
        self.play(
            FadeIn(cerebro_izq),
            FadeIn(cerebro_der),
            FadeIn(etq_izq),
            FadeIn(etq_der),
            run_time=1.0
        )
        
        # Cambio de expresión del protagonista para indicar revelación
        cambiar_cara(prota, "sorpresa")
        
        # Usamos etiqueta() en lugar de callout con coordenadas flotantes correctas (tupla x, y)
        c = etiqueta("¡No son iguales!", pos=(3.6, 1.2), color=ORANGE, font_size=50)
        self.play(FadeIn(c))
        
        self.wait(5.0)