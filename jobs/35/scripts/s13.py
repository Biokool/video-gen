from manim import *
from zenn_rig import *

class S13(Scene):
    def construct(self):
        self.add(fondo(AZUL_MARINO))
        
        # Título superior seguro con banda (usando el objeto devuelto con FadeIn)
        tb = banda_titulo("Una orquesta de notas", color=MOSTAZA)
        self.play(FadeIn(tb))
        
        # Protagonista abajo a la izquierda con expresión pensativa
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_AZUL, altura=2.4, expresion="pensando", pose="de_pie")
        self.play(FadeIn(prota))
        
        # Grupo de monigotes simulando músicos a la derecha
        musicos = stick_group(n=3, center=RIGHT*3.5+DOWN*0.5, spacing=1.2, height=2.0, color=WHITE)
        self.play(FadeIn(musicos))
        
        # Uso de etiqueta() en lugar de callout para evitar llamadas redundantes de texto destacado
        c = etiqueta("Cada uno con su tono", pos=RIGHT*3.5+UP*1.2, color=CORAL, font_size=40)
        self.play(FadeIn(c))
        
        self.wait(2.5)