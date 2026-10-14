from manim import *
from zenn_rig import *

class S13(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        titulo = banda_titulo("Lateralidad y Asimetría", color=AZUL_MARINO)
        self.play(
            FadeIn(titulo),
            run_time=0.5
        )
        
        prota = protagonista(
            pos=DOWN * 1.2 + LEFT * 3.5,
            playera=PLAYERA_AZUL,
            altura=2.6,
            expresion="alegria_pura",
            pose="senalando"
        )
        
        cerebro_icono = matraz(pos=RIGHT * 3.2 + DOWN * 1.2, escala=1.2, liquido=TEAL)
        
        self.play(
            FadeIn(prota),
            FadeIn(cerebro_icono),
            run_time=1.0
        )
        
        cambiar_cara(prota, "decidido")
        self.wait(2.0)
        
        self.play(
            FadeOut(prota),
            FadeOut(cerebro_icono),
            FadeOut(titulo),
            run_time=0.5
        )