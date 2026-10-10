from manim import *
from zenn_rig import *

class S109(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.5, 
            playera=PLAYERA_NARANJA, 
            altura=2.4, 
            expresion='pensando', 
            pose='de_pie'
        )
        
        self.play(FadeIn(prota, shift=UP))
        
        titulo = titulo_seguro("¿Eres zurdo o diestro?", color=INK, font_size=52, y=2.2)
        self.play(Write(titulo))
        
        caja_izq = caja("ZURDO", pos=RIGHT * 2.0 + UP * 0.5, width=2.0)
        caja_der = caja("DIESTRO", pos=RIGHT * 4.8 + UP * 0.5, width=2.0)
        
        self.play(
            Create(caja_izq),
            Create(caja_der),
            run_time=1.0
        )
        
        cambiar_cara(prota, 'sorpresa')
        
        self.wait(1.0)