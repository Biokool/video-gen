from manim import *
from zenn_rig import *

class S26(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título superior seguro (ÚNICO elemento de título/banda para evitar solapamientos)
        self.add(banda_titulo("La lateralidad es un espectro", color=TEAL))
        
        # Protagonista abajo a la izquierda (evitando zona superior y subtítulos)
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*3.8,
            playera=PLAYERA_VERDE,
            altura=2.4,
            expresion="pensando",
            pose="senalando"
        )
        self.add(prota)
        
        # Gráfica de barras representando el espectro de lateralidad a la derecha
        graf = grafica_barras(
            pos=RIGHT*2.8 + DOWN*0.3,
            valores=(2, 5, 8, 4, 1),
            ancho=4.0,
            color=TEAL,
            etiquetas=("Zurdo", "Mixto", "Diestro", "Mixto", "Zurdo")
        )
        self.play(Create(graf), run_time=1.5)
        
        # Nota: Se eliminó el callout redundante para cumplir estrictamente con la regla
        # de tener solo UN elemento tipo banda/título/callout principal por escena.
        # Usamos una etiqueta pequeña para información secundaria.
        etq = etiqueta("No es tan simple", pos=RIGHT*3.2 + UP*1.2, color=ORANGE, font_size=36)
        self.play(FadeIn(etq), run_time=0.8)
        
        # Cambio dinámico de expresión en el protagonista utilizando cambiar_cara correctamente
        cambiar_cara(prota, "alegria_pura")
        
        self.wait(2.2)