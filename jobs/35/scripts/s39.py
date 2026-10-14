from manim import *
from zenn_rig import *

class S39(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        # Título seguro en la zona superior (ÚNICO título/callout principal)
        titulo = titulo_seguro("Factores sociales y culturales", color=INK)
        self.play(Write(titulo))
        
        # Protagonista abajo a la izquierda para dejar espacio
        prota = protagonista(pos=DOWN*1.5 + LEFT*3.5, playera=PLAYERA_AZUL, altura=2.4, expresion='pensando', pose='de_pie')
        self.play(FadeIn(prota))
        
        # Etiquetas representativas como elementos secundarios (permitidas sin chocar con título)
        etq_cultura = etiqueta("Cultura", pos=UP*0.5 + RIGHT*2.0, color=RED, font_size=40)
        etq_aprendizaje = etiqueta("Aprendizaje", pos=DOWN*0.5 + RIGHT*2.0, color=RED, font_size=40)
        
        flecha1 = arrow(prota.get_top(), etq_cultura.get_center(), color=INK, width=6)
        flecha2 = arrow(prota.get_center(), etq_aprendizaje.get_center(), color=INK, width=6)
        
        self.play(
            FadeIn(etq_cultura, shift=UP*0.3),
            FadeIn(etq_aprendizaje, shift=DOWN*0.3),
            Create(flecha1),
            Create(flecha2),
            run_time=1.5
        )
        
        # Cambio de expresión del protagonista
        cambiar_cara(prota, 'confundido')
        
        # Usamos etiqueta secundaria en lugar de callout para evitar duplicidad de elementos grandes de texto
        etq_extra = etiqueta("Autopercepción condicionada", pos=RIGHT*3.5 + UP*1.0, color=ORANGE, font_size=40)
        self.play(FadeIn(etq_extra), run_time=1.0)
        
        self.wait(2.5)