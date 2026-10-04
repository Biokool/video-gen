from manim import *
from zenn_rig import *

class S08(Scene):
    def construct(self):
        # Título seguro en la zona superior
        titulo = titulo_seguro("La Realidad Científica", color=AZUL_MARINO, y=2.8)
        
        # Protagonista con playera azul (BLUE) y expresión pensativa
        prota = protagonista(
            pos=LEFT * 2 + DOWN * 0.5, 
            playera=BLUE, 
            altura=3.0, 
            expresion='pensando', 
            pose='de_pie'
        )
        
        # Matraz científico con líquido TEAL
        flask = matraz(
            pos=RIGHT * 1.8 + DOWN * 0.5, 
            escala=1.4, 
            liquido=TEAL
        )
        
        # Aparecen el título y el protagonista
        self.play(FadeIn(titulo))
        self.play(FadeIn(prota, shift=RIGHT))
        self.wait(0.5)
        
        # Aparece el matraz
        self.play(Create(flask))
        
        # Acento visual rojo para destacar el matraz
        acento = red_accent(flask, scale=1.3)
        self.play(FadeIn(acento))
        
        # El protagonista cambia su expresión a decidido al ver la ciencia
        cambiar_cara(prota, 'decidido')
        self.wait(1.8)
        
        # Salida de la escena
        self.play(
            FadeOut(titulo),
            FadeOut(prota),
            FadeOut(flask),
            FadeOut(acento)
        )
        self.wait(0.5)