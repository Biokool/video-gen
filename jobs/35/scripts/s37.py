from manim import *
from zenn_rig import *

class S37(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título seguro arriba (Creamos el objeto y usamos Write o FadeIn, NO se pasa directamente a play())
        t_seguro = titulo_seguro("¡El Viaje del Conocimiento!", color=INK, y=2.5)
        self.play(Write(t_seguro))
        
        # Protagonista abajo a la izquierda (evita zona de título y respeta zona de subtítulos)
        prota = protagonista(pos=DOWN*1.5 + LEFT*3.8, playera=PLAYERA_NARANJA, altura=2.4, expresion="alegria_pura", pose="senalando")
        self.play(FadeIn(prota))
        
        # Objeto temático a la derecha (separado del protagonista)
        obj_matraz = matraz(pos=RIGHT*3.5 + DOWN*0.5, escala=1.2, liquido=TEAL)
        self.play(Create(obj_matraz))
        
        # Usamos etiqueta para texto secundario seguro
        etq = etiqueta("¡Ciencia en acción!", pos=RIGHT*3.5 + UP*1.2, color=ORANGE, font_size=40, ancho_max=5.5)
        self.play(FadeIn(etq))
        
        # Pequeña animación de interacción
        cambiar_cara(prota, "mente_explotada")
        self.wait(2.5)