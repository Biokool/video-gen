from manim import *
from zenn_rig import *

class S83(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título superior seguro (único en la escena)
        self.add(banda_titulo("Cerebro que se Adapta al Uso", color=ORANGE))
        
        # Protagonista abajo a la izquierda (evita banda y zona de subtítulos)
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.8,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="alegria_pura",
            pose="senalando"
        )
        self.add(prota)
        
        # Props a la derecha: un ADN y una flecha indicadora
        cerebro_obj = adn(pos=RIGHT * 3.5 + UP * 0.2, escala=1.2, color=TEAL)
        flechita = arrow(start=LEFT * 1.5 + UP * 0.2, end=RIGHT * 1.5 + UP * 0.2, color=INK, width=8)
        
        # Uso de etiqueta() en lugar de callout para evitar llamadas conflictivas de texto destacado
        et = etiqueta("¡La práctica refuerza conexiones!", pos=RIGHT * 3.4 + UP * 1.8, color=RED, font_size=40, ancho_max=5.5)
        
        self.play(FadeIn(cerebro_obj), Create(flechita), FadeIn(et), run_time=1.5)
        
        # Pequeña animación del protagonista cambiando de expresión (usando animación individual soportada)
        cambiar_cara(prota, "mente_explotada")
        
        self.wait(5.5)