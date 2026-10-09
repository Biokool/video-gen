from manim import *
from zenn_rig import *

class S30(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        self.play(FadeIn(banda_titulo("¡Un éxito rotundo en la ópera!", color=CORAL)))
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*3.8,
            playera=PLAYERA_ROSA,
            altura=2.4,
            expresion="alegria_pura",
            pose="senalando"
        )
        self.play(FadeIn(prota))
        
        casco = casco_vikingo(pos=RIGHT*2.5 + UP*0.8, escala=1.4)
        moneda = moneda_dorada(texto="★", pos=RIGHT*4.8 + UP*0.2, radio=0.7)
        self.play(Create(casco), FadeIn(moneda))
        
        et = etiqueta("¡Éxito colectivo!", pos=RIGHT*3.6 + DOWN*1.2, color=MOSTAZA)
        self.play(FadeIn(et))
        
        self.play(
            casco.animate.scale(1.1),
            moneda.animate.rotate(0.2),
            run_time=1.0
        )
        
        self.wait(5.0)