from manim import *
from zenn_rig import *

class S29(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera=PLAYERA_AMARILLA, 
            altura=2.5, 
            expresion='pensando', 
            pose='de_pie'
        )
        
        moneda = moneda_dorada(texto='$', pos=UP*0.5 + RIGHT*2.5, radio=1.0)
        c = callout("Genes y hormonas cargan la moneda", color=ORANGE, pos=RIGHT*3.0 + DOWN*1.5)
        
        self.play(FadeIn(prota), Create(moneda))
        self.play(
            moneda.animate.shift(UP*1.5).rotate(3.14),
            run_time=1.5
        )
        self.play(FadeIn(c))
        
        cambiar_cara(prota, 'sorpresa')
        self.play(
            moneda.animate.shift(DOWN*1.5),
            run_time=1.5
        )
        
        self.wait(2.0)