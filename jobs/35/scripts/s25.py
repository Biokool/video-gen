from manim import *
from zenn_rig import *

class S25(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        titulo = banda_titulo("¡Hemisferio derecho al mando!", color=TEAL)
        self.play(FadeIn(titulo))
        
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_VERDE, altura=2.4, expresion='sorpresa', pose='senalando')
        self.play(FadeIn(prota))
        
        cerebro = planeta(pos=RIGHT*3.0+UP*0.3, radio=1.4, color=TEAL)
        self.play(FadeIn(cerebro))
        
        nota = etiqueta("¡Sorpresa para zurdos!", pos=RIGHT*3.2+UP*1.8, color=ORANGE, font_size=40)
        self.play(FadeIn(nota))
        
        self.wait(3.0)
        
        cambiar_cara(prota, 'alegria_pura')
        self.play(prota.animate.shift(UP*0.2), run_time=0.5)
        self.wait(2.0)
        
        self.play(FadeOut(prota), FadeOut(cerebro), FadeOut(nota), FadeOut(titulo))