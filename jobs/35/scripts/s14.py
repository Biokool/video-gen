from manim import *
from zenn_rig import *

class S14(Scene):
    def construct(self):
        self.add(fondo(AZUL_MARINO))
        
        self.play(
            FadeIn(banda_titulo("MÁS DE 40 GENES IDENTIFICADOS", color=TEAL)),
            run_time=0.8
        )
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera=PLAYERA_AZUL, 
            altura=2.5, 
            expresion='mente_explotada', 
            pose='senalando'
        )
        self.play(FadeIn(prota), run_time=0.8)
        
        dna = adn(pos=RIGHT*2.5 + UP*0.3, escala=1.2, color=TEAL)
        self.play(Create(dna), run_time=1.0)
        
        box = caja(etiqueta="40+ GENES", pos=RIGHT*2.5 + DOWN*1.5, width=2.0)
        self.play(FadeIn(box), run_time=0.8)
        
        e = etiqueta("Héca et al., 2014", pos=RIGHT*3.2 + UP*1.8, color=WHITE, font_size=36)
        self.play(FadeIn(e), run_time=0.8)
        
        self.wait(5.0)
        
        self.play(
            FadeOut(prota),
            FadeOut(dna),
            FadeOut(box),
            FadeOut(e),
            run_time=0.8
        )