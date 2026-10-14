from manim import *
from zenn_rig import *

class S47(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        tc = tarjeta_canal(texto="INDAGA", subtitulo="nos vemos en el próximo video")
        self.play(FadeIn(tc, scale=0.9), run_time=1.0)
        self.wait(1.5)
        
        prota = protagonista(pos=DOWN*1.2+RIGHT*3.5, playera=AZUL_MARINO, altura=2.4, expresion='alegria_pura', pose='de_pie')
        self.play(FadeIn(prota), run_time=1.0)
        
        et = etiqueta("¡Hasta la próxima indagación!", pos=LEFT*2.8+UP*0.5)
        self.play(FadeIn(et), run_time=0.8)
        
        cambiar_cara(prota, 'euforico')
        self.wait(1.7)