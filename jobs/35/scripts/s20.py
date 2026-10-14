from manim import *
from zenn_rig import *

class S20(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.3+LEFT*4.0, 
            playera=PLAYERA_ROSA, 
            altura=2.4, 
            expresion='pensando', 
            pose='de_pie'
        )
        
        c = callout("Negociación constante", color=ORANGE, pos=RIGHT*3.2+UP*1.0)
        
        cerebro_izq = planeta(pos=LEFT*0.8+UP*0.5, radio=1.1, color=TEAL)
        cerebro_der = planeta(pos=RIGHT*1.8+UP*0.5, radio=1.1, color=CORAL)
        f_izq = fuego(pos=LEFT*0.8+UP*0.5, escala=0.8)
        
        msg = etiqueta("Lados del cerebro", pos=UP*2.2, color=INK, font_size=38)
        
        self.play(
            FadeIn(prota),
            FadeIn(cerebro_izq),
            FadeIn(cerebro_der),
            FadeIn(f_izq),
            FadeIn(msg),
            run_time=1.0
        )
        
        cambiar_cara(prota, 'sorpresa')
        
        self.play(
            FadeIn(c),
            run_time=1.0
        )
        
        self.play(
            prota.animate.shift(RIGHT*0.5),
            run_time=1.5
        )
        
        self.wait(2.5)