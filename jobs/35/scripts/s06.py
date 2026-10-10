from manim import *
from zenn_rig import *

class S06(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        # Título seguro en la zona superior
        titulo = banda_titulo("BATALLA EN EL CEREBRO", color=ORANGE)
        self.play(FadeIn(titulo))
        
        # Protagonista abajo a la izquierda, mirando y señalando hacia el centro
        prota = protagonista(
            pos=DOWN * 1.3 + LEFT * 3.5, 
            playera=PLAYERA_NARANJA, 
            altura=2.4, 
            expresion='pensando', 
            pose='senalando'
        )
        self.play(FadeIn(prota))
        
        # Prop temático a la derecha (matraz)
        cerebro_obj = matraz(pos=RIGHT * 3.2 + UP * 0.2, escala=1.2, liquido=TEAL)
        self.play(Create(cerebro_obj))
        
        # Usamos etiqueta en lugar de callout adicional para evitar duplicidad de elementos de texto destacado
        dato = etiqueta("¡Guerra silenciosa!", pos=RIGHT * 3.2 + UP * 1.8, color=RED)
        self.play(FadeIn(dato))
        
        # Animación sutil de desplazamiento y cambio de expresión
        self.play(
            prota.animate.shift(RIGHT * 0.3),
            run_time=1.0
        )
        cambiar_cara(prota, 'sorpresa')
        
        self.wait(3.5)