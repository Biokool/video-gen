from manim import *
from zenn_rig import *

class S80(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera=PLAYERA_ROJA, 
            altura=2.6, 
            expresion='pensando', 
            pose='brazos_cruzados'
        )
        
        titulo = banda_titulo("¿Qué otras verdades son maleables?", color=ORANGE)
        
        c = caja(etiqueta="¿?", pos=RIGHT*3.0 + UP*0.5, width=2.0)
        p = planeta(pos=RIGHT*3.0 + DOWN*1.5, radio=1.0, color=TEAL)
        
        self.play(
            FadeIn(prota),
            FadeIn(titulo),
            FadeIn(c),
            FadeIn(p),
            run_time=1.5
        )
        
        cambiar_cara(prota, 'mente_explotada')
        
        self.play(
            p.animate.shift(UP*0.3),
            run_time=2.0
        )
        
        self.wait(7.5)