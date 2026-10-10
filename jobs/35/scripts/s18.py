from manim import *
from zenn_rig import *

class S18(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(pos=DOWN*1.4+LEFT*3.5, playera=PLAYERA_AZUL, altura=2.4, expresion='sorpresa', pose='senalando')
        
        hormona1 = fuego(pos=UP*1.0+RIGHT*1.0, escala=0.8)
        hormona2 = fuego(pos=UP*0.2+RIGHT*2.5, escala=0.8)
        
        c = callout("¿Zurdo o diestro?\nInfluencia prenatal", color=AZUL_MARINO, pos=RIGHT*3.2+UP*1.5)
        
        self.play(FadeIn(prota), FadeIn(hormona1), FadeIn(hormona2), Create(c), run_time=1.5)
        cambiar_cara(prota, 'mente_explotada')
        self.wait(6.5)