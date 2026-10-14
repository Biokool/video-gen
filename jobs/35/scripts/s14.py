from manim import *
from zenn_rig import *

class S14(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        self.add(banda_titulo("Hemisferios cerebrales", color=TEAL))
        
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.8,
            playera=PLAYERA_VERDE,
            altura=2.4,
            expresion="sorpresa",
            pose="senalando"
        )
        self.add(prota)
        
        cerebro = red_seguridad(width=3.0, height=1.5, pos=UP * 0.5 + RIGHT * 2.5)
        self.add(cerebro)
        
        fig = stick_idle(pos=DOWN * 1.5 + RIGHT * 3.5, height=2.2, color=INK)
        self.add(fig)
        
        flecha1 = arrow(UP * 0.2 + RIGHT * 1.8, DOWN * 0.8 + RIGHT * 2.8, color=RED, width=8)
        flecha2 = arrow(UP * 0.2 + RIGHT * 3.2, DOWN * 0.8 + RIGHT * 2.2, color=BLUE, width=8)
        self.add(flecha1, flecha2)
        
        txt_dato = etiqueta("Cruzado", pos=UP * 1.8 + LEFT * 2.5, color=ORANGE, font_size=40)
        self.add(txt_dato)
        
        cambiar_cara(prota, "alegria_pura")
        self.wait(2.5)