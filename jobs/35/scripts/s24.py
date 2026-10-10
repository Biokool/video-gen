from manim import *
from zenn_rig import *

class S24(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.2+LEFT*3.5, 
            playera=PLAYERA_VERDE, 
            altura=2.6, 
            expresion='decidido', 
            pose='senalando'
        )
        
        self.play(FadeIn(prota), run_time=0.5)
        
        tb = banda_titulo("HEMISFERIO IZQUIERDO", color=TEAL)
        self.play(Write(tb), run_time=1.0)
        
        mat = matraz(pos=RIGHT*3.5+UP*0.2, escala=1.2, liquido=TEAL)
        cerebro_lupo = lupa(pos=RIGHT*3.5+UP*0.2, escala=1.2, color=INK)
        
        self.play(Create(mat), FadeIn(cerebro_lupo), run_time=1.0)
        
        etq = etiqueta("¡Dominante para lenguaje!", pos=RIGHT*3.2+UP*1.8, color=ORANGE)
        self.play(FadeIn(etq), run_time=0.8)
        
        cambiar_cara(prota, 'alegria_pura')
        
        self.wait(3.7)