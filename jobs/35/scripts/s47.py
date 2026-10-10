from manim import *
from zenn_rig import *

class S47(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        titulo = banda_titulo("EL MISTERIO DEL TIEMPO", color=AZUL_MARINO)
        self.play(FadeIn(titulo))
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera=PLAYERA_AZUL, 
            altura=2.6, 
            expresion="confundido", 
            pose="de_pie"
        )
        self.play(FadeIn(prota))
        
        reloj = reloj_pared(radius=1.2, pos=RIGHT*3.5 + UP*0.5, hora_3=True)
        self.play(Create(reloj))
        
        etq = etiqueta("¿El tiempo vuela?", pos=RIGHT*3.2 + DOWN*1.5, color=ORANGE)
        self.play(FadeIn(etq))
        
        cambiar_cara(prota, "sorpresa")
        
        self.wait(1.5)