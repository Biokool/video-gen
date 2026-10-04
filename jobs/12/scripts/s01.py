from manim import *
from zenn_rig import *

class S01(Scene):
    def construct(self):
        # Crear la tarjeta de canal "EL PORQUÉ"
        channel_card = tarjeta_canal(texto='EL PORQUÉ', subtitulo='curiosidad científica')
        
        # Crear el monigote y su expresión "feliz"
        stick_figure = stick_idle(height=2.2, color=INK)
        happy_expression = expresion(stick_figure, tipo='feliz')
        
        # Agrupar el monigote con su expresión para moverlos juntos
        stick_group = VGroup(stick_figure, happy_expression)
        
        # Posicionar la tarjeta de canal a la izquierda y el monigote a la derecha
        channel_card.move_to(LEFT * 3.5)
        stick_group.move_to(RIGHT * 3.5)
        
        # Centrar verticalmente ambos elementos para evitar la zona de subtítulos
        channel_card.shift(UP * 0.5)
        stick_group.shift(UP * 0.5)

        # Animación de entrada de los elementos
        self.play(
            FadeIn(channel_card, shift=LEFT),
            FadeIn(stick_group, shift=RIGHT),
            run_time=1.5
        )
        
        # Mantener la escena visible por unos segundos
        self.wait(6) # Total ~9s (1.5s entrada + 6s espera + 1.5s salida)
        
        # Animación de salida de los elementos
        self.play(
            FadeOut(channel_card, shift=RIGHT),
            FadeOut(stick_group, shift=LEFT),
            run_time=1.5
        )