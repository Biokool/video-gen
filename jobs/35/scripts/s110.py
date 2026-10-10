from manim import *
from zenn_rig import *

class S110(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título superior seguro (una sola llamada al sistema de títulos)
        self.add(banda_titulo("La decisión antes de nacer", color=ORANGE))
        
        # Protagonista abajo a la izquierda para evitar solapes
        prota = protagonista(pos=DOWN*1.2 + LEFT*3.5, playera=PLAYERA_AZUL, altura=2.6, expresion="pensando", pose="de_pie")
        
        # Prop temático a la derecha (ADN)
        dna = adn(pos=RIGHT*3.5 + UP*0.2, escala=1.1, color=TEAL)
        
        # Usamos etiqueta en lugar de callout simultáneo para evitar solapar múltiples cajas de texto
        etq = etiqueta("¡Predestinado!", pos=RIGHT*3.2 + UP*1.2, color=RED)
        
        self.play(
            FadeIn(prota),
            Create(dna),
            FadeIn(etq),
            run_time=1.5
        )
        
        # Pequeña animación de cambio de expresión (cambiar_cara modifica el mobject sin pasar por Scene.play)
        cambiar_cara(prota, "sorpresa")
        
        self.wait(1.5)