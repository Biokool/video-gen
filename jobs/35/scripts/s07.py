from manim import *
from zenn_rig import *

class S07(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        self.add(banda_titulo("Genes y Probabilidad", color=ORANGE))
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_VERDE,
            altura=2.4,
            expresion="pensando",
            pose="senalando"
        )
        
        balanza = moneda_dorada(texto="⚖", pos=RIGHT*3.0 + UP*0.2, radio=1.2)
        
        ref_texto = etiqueta(
            "Héca et al., 2014\nFrontiers in Psych.", 
            pos=RIGHT*3.0 + DOWN*1.8, 
            font_size=28
        )
        
        flecha = arrow(start=LEFT*1.8 + UP*0.5, end=RIGHT*1.5 + UP*0.5, color=INK, width=6)
        
        self.play(
            FadeIn(prota),
            FadeIn(balanza),
            Create(flecha),
            FadeIn(ref_texto),
            run_time=1.5
        )
        
        cara_nueva = cambiar_cara(prota, "alegria_pura")
        self.play(FadeIn(cara_nueva), run_time=0.5)
        self.wait(9.0)