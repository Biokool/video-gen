from manim import *
from zenn_rig import *

class S34(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(pos=DOWN*1.2+LEFT*4.0, playera=PLAYERA_ROSA, altura=2.4, expresion='confundido', pose='de_pie')
        
        billete = moneda_dorada(texto='$$', pos=UP*0.5+LEFT*0.8, radio=0.8)
        dado = caja(etiqueta='SUERTE', pos=UP*0.5+RIGHT*2.5, width=1.5)
        
        c = callout("¿Lotería biológica?", color=ORANGE, pos=RIGHT*3.5+UP*1.8)
        
        self.play(
            FadeIn(prota),
            FadeIn(billete),
            FadeIn(dado),
            FadeIn(c),
            run_time=1.5
        )
        
        cambiar_cara(prota, 'mente_explotada')
        self.play(
            prota.animate.shift(RIGHT*0.5),
            run_time=2.0
        )
        
        self.wait(4.5)