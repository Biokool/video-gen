from manim import *
from zenn_rig import *

class S108(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN * 1.3 + LEFT * 4.0,
            playera=PLAYERA_AZUL,
            altura=2.5,
            expresion='sorpresa',
            pose='senalando'
        )
        
        titulo = banda_titulo("Right Hand, Left Hand — 2002", color=ORANGE)
        
        lib = caja(etiqueta="McManus", pos=RIGHT * 2.5 + DOWN * 0.2, width=2.0)
        cal = calendario(pos=RIGHT * 2.5 + UP * 1.5, width=1.8)
        
        self.play(
            FadeIn(prota),
            FadeIn(titulo),
            Create(lib),
            Create(cal),
            run_time=1.5
        )
        
        et = etiqueta("¡Un clásico!", pos=RIGHT * 3.4 + DOWN * 1.5, color=CORAL)
        self.play(FadeIn(et), run_time=1.0)
        
        self.wait(3.5)