from manim import *
from zenn_rig import *

class S93(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título seguro en la parte superior (único elemento de título/banda)
        self.add(banda_titulo("¿Zurdos o diestros?", color=ORANGE))
        
        # Protagonista abajo a la izquierda (evitando zona de banda y subtítulos)
        prota = protagonista(pos=DOWN*1.2 + LEFT*3.5, playera=PLAYERA_AZUL, altura=2.6, expresion="pensando", pose="de_pie")
        self.add(prota)
        
        # Cerebro o prop relevante a la derecha
        cerebro_prop = matraz(pos=RIGHT*3.5 + UP*0.2, escala=1.2, liquido=TEAL)
        self.add(cerebro_prop)
        
        # Usamos etiqueta en lugar de callout para evitar llamadas múltiples a elementos de texto tipo banner/caja superior
        lbl = etiqueta("¿Cómo es posible?", pos=RIGHT*3.4 + UP*1.8, color=TEAL, font_size=40)
        self.add(lbl)
        
        # Animación de entrada y cambio de expresión
        self.play(FadeIn(cerebro_prop), FadeIn(lbl), run_time=1.0)
        self.play(
            ApplyMethod(prota.shift, UP*0.2),
            run_time=0.8
        )
        cambiar_cara(prota, "sorpresa")
        
        self.wait(8.2)