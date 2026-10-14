from manim import *
from zenn_rig import *

class S03(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera=PLAYERA_AZUL, 
            altura=2.5, 
            expresion='pensando', 
            pose='de_pie'
        )
        
        lap = lapida(texto='LÁPIZ', pos=RIGHT*2.5 + DOWN*0.5)
        reloj = reloj_pared(radius=0.8, pos=RIGHT*2.5 + UP*1.8, hora_3=True)
        
        txt_banda = banda_titulo("¿Con qué mano escribes?", color=ORANGE)
        
        self.play(
            FadeIn(txt_banda),
            FadeIn(prota),
            Create(lap),
            FadeIn(reloj),
            run_time=1.5
        )
        
        cambiar_cara(prota, 'sorpresa')
        self.wait(2.0)
        
        self.wait(4.0)
        
        self.play(
            FadeOut(txt_banda),
            FadeOut(prota),
            FadeOut(lap),
            FadeOut(reloj),
            run_time=1.0
        )