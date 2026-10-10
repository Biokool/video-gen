from manim import *
from zenn_rig import *

class S19(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título seguro superior y personaje principal abajo
        self.play(
            FadeIn(banda_titulo("Genética + Ambiente = ¿Zurdo o Diestro?", color=ORANGE)),
            FadeIn(protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_AZUL, altura=2.6, expresion="pensando", pose="de_pie"))
        )
        
        # Elementos visuales complementarios en el lado derecho
        dna_obj = adn(pos=RIGHT*3.0+UP*0.5, escala=0.8, color=TEAL)
        casa_obj = casa(pos=RIGHT*4.5+DOWN*1.0, size=1.2)
        flecha_1 = arrow(start=DOWN*1.0+LEFT*1.5, end=RIGHT*2.0+UP*0.5, color=INK, width=6)
        
        # Usamos etiqueta en lugar de callout para evitar llamadas múltiples a títulos
        etq = etiqueta("¿Cómo se unen?", pos=RIGHT*3.2+UP*2.0, color=ORANGE, font_size=40)
        
        self.play(
            Create(dna_obj),
            FadeIn(casa_obj),
            Create(flecha_1),
            FadeIn(etq)
        )
        self.wait(3.5)