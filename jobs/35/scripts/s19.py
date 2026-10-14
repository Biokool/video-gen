from manim import *
from zenn_rig import *

class S19(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_AMARILLA, altura=2.4, expresion='pensando', pose='de_pie')
        
        izq = stick_idle(pos=UP*0.5+LEFT*0.5, height=2.2, color=INK)
        der = stick_idle(pos=UP*0.5+RIGHT*2.5, height=2.2, color=INK)
        expresion(izq, 'feliz')
        expresion(der, 'sorpresa')
        
        f1 = arrow(izq.get_right(), der.get_left(), color=ORANGE, width=8)
        f2 = arrow(der.get_left(), izq.get_right(), color=TEAL, width=8)
        
        self.play(
            FadeIn(prota),
            FadeIn(izq),
            FadeIn(der),
            Create(f1),
            Create(f2),
            run_time=1.0
        )
        
        c = callout("¡Dominancia cruzada!", color=ORANGE, pos=RIGHT*3.6+UP*1.5)
        
        cambiar_cara(prota, 'mente_explotada')
        
        self.play(
            FadeIn(c),
            run_time=1.0
        )
        
        self.wait(6.0)