from manim import *
from zenn_rig import *

class S27(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera=PLAYERA_AMARILLA, 
            altura=2.6, 
            expresion='confundido', 
            pose='de_pie'
        )
        
        dado = caja(etiqueta="AZAR", pos=UP*2.5 + RIGHT*3.0, width=1.5)
        balanza = grafica_barras(pos=DOWN*1.0 + RIGHT*3.0, valores=(3, 5), ancho=3.0, color=TEAL)
        
        texto_llamado = callout("¡El Factor X!", color=ORANGE, pos=RIGHT*3.2 + UP*1.0)
        
        self.play(FadeIn(prota), FadeIn(dado), FadeIn(balanza))
        cambiar_cara(prota, 'pensando')
        self.play(Create(texto_llamado), run_time=1.0)
        
        flecha_caida = arrow(UP*2.0 + RIGHT*3.0, DOWN*0.2 + RIGHT*3.0, color=RED)
        self.play(Create(flecha_caida), run_time=0.8)
        
        cambiar_cara(prota, 'sorpresa')
        self.wait(2.5)