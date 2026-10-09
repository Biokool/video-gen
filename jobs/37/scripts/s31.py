from manim import *
from zenn_rig import *

class S31(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Banda de título principal (única permitida para evitar encimar textos principales)
        banda = banda_titulo("El mito del arte", color=CORAL)
        self.play(FadeIn(banda, shift=DOWN * 0.3))

        # Protagonista en la parte inferior izquierda
        prota = protagonista(pos=DOWN * 1.2 + LEFT * 3.5, playera="verde", altura=2.4, expresion="feliz", pose="senalando")
        self.play(FadeIn(prota, shift=UP * 0.5))

        # Elementos de escena en el lado derecho
        rollo = caja("CINE", pos=RIGHT * 2.2 + UP * 1.0, width=1.3)
        comic = caja("CÓMIC", pos=RIGHT * 4.5 + UP * 1.0, width=1.3)
        calabaza = personaje(pos=RIGHT * 3.35 + UP * 2.3, cuerpo=CORAL, altura=1.4, expresion_tipo="feliz")

        self.play(
            FadeIn(rollo, shift=DOWN * 0.4), 
            FadeIn(comic, shift=DOWN * 0.4), 
            FadeIn(calabaza, shift=DOWN * 0.4)
        )
        self.wait(1.5)

        # Cambio de expresión y animación corregida sin usar Transform(x, x.animate)
        cambiar_cara(prota, "sorpresa")
        self.play(
            rollo.animate.shift(UP * 0.15),
            comic.animate.shift(DOWN * 0.15),
            calabaza.animate.shift(UP * 0.1),
            run_time=1.0
        )
        self.wait(1.0)

        # Usamos etiqueta() para la idea secundaria, evitando el conflicto con banda_titulo
        idea_texto = etiqueta("El arte creó el mito", pos=RIGHT * 3.3 + DOWN * 1.2, color=AZUL_MARINO, font_size=36)
        self.play(FadeIn(idea_texto, shift=LEFT * 0.2))
        self.wait(1.5)

        # Cambio final de cara y salida de la etiqueta
        cambiar_cara(prota, "alegria_pura")
        self.play(FadeOut(idea_texto), run_time=0.5)
        self.wait(0.5)