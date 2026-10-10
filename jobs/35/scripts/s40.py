from manim import *
from zenn_rig import *

class S40(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        titulo = banda_titulo("¿Por qué soñamos?", color=ORANGE)
        self.play(
            FadeIn(titulo),
            run_time=0.5
        )
        
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.5, 
            playera=PLAYERA_MORADA, 
            altura=2.4, 
            expresion='pensando', 
            pose='de_pie'
        )
        
        c = reloj_pared(radius=1.1, pos=RIGHT * 3.5 + UP * 0.2, hora_3=True)
        
        self.play(
            FadeIn(prota),
            Create(c),
            run_time=1.0
        )
        
        cambiar_cara(prota, 'mente_explotada')
        
        self.wait(2.0)