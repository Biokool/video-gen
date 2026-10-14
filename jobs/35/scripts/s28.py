from manim import *
from zenn_rig import *

class S28(Scene):
    def construct(self):
        self.add(fondo(AZUL_MARINO))
        
        titulo = banda_titulo("El factor decisivo: Conexiones", color=YELLOW)
        self.play(
            FadeIn(titulo),
            run_time=0.5
        )
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.8,
            playera=PLAYERA_AMARILLA,
            altura=2.4,
            expresion="sorpresa",
            pose="senalando"
        )
        self.play(FadeIn(prota), run_time=0.8)
        
        red = adn(pos=RIGHT*3.0 + UP*0.3, escala=1.2, color=TEAL)
        f = fuego(pos=RIGHT*2.0 + DOWN*1.5, escala=0.8)
        
        self.play(
            Create(red),
            FadeIn(f),
            run_time=1.0
        )
        
        co = etiqueta("¡Aleatoriedad pura!", pos=RIGHT*3.5 + UP*1.8, color=ORANGE)
        self.play(FadeIn(co), run_time=0.8)
        
        cambiar_cara(prota, "mente_explotada")
        self.wait(0.5)
        
        self.wait(3.4)