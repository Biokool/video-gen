from manim import *
from zenn_rig import *

class S74(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título seguro en la parte superior (una sola vez)
        self.add(banda_titulo("Factores Sociales y de Aprendizaje", color=ORANGE))
        
        # Protagonista abajo a la izquierda, mirando hacia la derecha
        prota = protagonista(pos=DOWN*1.2 + LEFT*3.5, playera=PLAYERA_AZUL, altura=2.4, expresion='pensando', pose='de_pie')
        self.add(prota)
        
        # Monigote secundario realizando una acción
        fig = stick_idle(pos=RIGHT*1.0 + DOWN*1.0, height=2.2, color=INK)
        expresion(fig, 'preocupado')
        self.add(fig)
        
        # Flechas indicadoras y etiquetas explicativas respetando las zonas seguras
        arr1 = arrow(start=LEFT*0.2 + UP*0.5, end=RIGHT*1.8 + UP*0.5, color=RED, width=6)
        etq1 = etiqueta("Influencia Social", (2.5, 0.8))
        
        arr2 = arrow(start=RIGHT*0.5 + DOWN*0.5, end=RIGHT*2.2 + DOWN*1.5, color=INK, width=6)
        etq2 = etiqueta("Castigo", (2.5, -1.8))
        
        # Nota: Se eliminó el callout para evitar llamadas duplicadas de elementos destacados en la misma escena.
        
        # Animaciones de entrada y movimiento
        self.play(
            FadeIn(fig),
            Create(arr1),
            FadeIn(etq1),
            run_time=1.5
        )
        
        self.play(
            stick_walk(fig, target=RIGHT*3.0 + DOWN*1.0),
            Create(arr2),
            FadeIn(etq2),
            run_time=3.5
        )
        
        self.wait(2.0)