from manim import *
from zenn_rig import *

class S10(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        # Título único y seguro
        titulo = banda_titulo("Lateralidad y Cerebro", color=AZUL_MARINO)
        self.play(Write(titulo))
        
        # Protagonista abajo a la izquierda (respetando la zona segura)
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 4.0, 
            playera=PLAYERA_AZUL, 
            altura=2.4, 
            expresion='pensando', 
            pose='de_pie'
        )
        self.play(FadeIn(prota))
        
        # Pantalla dividida para mostrar los dos hemisferios
        divs = split_screen("Izquierdo: Lenguaje", "Derecho: Motricidad")
        self.play(Create(divs), run_time=1.5)
        
        # Props explicativos en cada lado
        matraz_izq = matraz(pos=LEFT * 2.5 + UP * 0.5, escala=0.9, liquido=TEAL)
        cerebro_der = adn(pos=RIGHT * 2.5 + UP * 0.5, escala=0.9, color=CORAL)
        self.play(FadeIn(matraz_izq), FadeIn(cerebro_der))
        
        # Uso de etiqueta en lugar de un segundo elemento de texto grande (callout)
        info = etiqueta("¡Preferencia natural!", pos=RIGHT * 3.5 + UP * 1.8, color=ORANGE)
        self.play(FadeIn(info))
        
        # Cambio de expresión del protagonista para dinamismo
        cambiar_cara(prota, 'alegria_pura')
        self.wait(0.5)
        
        self.wait(4.0)
        
        # Limpieza de elementos finales
        self.play(
            FadeOut(prota),
            FadeOut(divs),
            FadeOut(matraz_izq),
            FadeOut(cerebro_der),
            FadeOut(info),
            FadeOut(titulo),
            run_time=1.0
        )