from manim import *
from zenn_rig import *

class S25(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        titulo = banda_titulo("Lateralidad y Testosterona", color=AZUL_MARINO)
        self.play(FadeIn(titulo))
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*3.8,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="pensando",
            pose="senalando"
        )
        self.play(FadeIn(prota))
        
        lab_matraz = matraz(pos=RIGHT*2.0 + DOWN*0.5, escala=1.2, liquido=ORANGE)
        cerebro_curva = curva(pos=RIGHT*3.0 + UP*1.2, ancho=3.0, alto=2.0, color=AZUL_MARINO, acento=RED)
        
        self.play(Create(lab_matraz), Create(cerebro_curva))
        
        flecha = arrow(start=RIGHT*1.2 + DOWN*0.5, end=RIGHT*2.2 + UP*0.5, color=INK, width=6)
        self.play(Create(flecha))
        
        cara_nueva = cambiar_cara(prota, "sorpresa")
        acento_rojo = red_accent(lab_matraz, scale=1.15)
        self.play(
            FadeIn(cara_nueva),
            FadeIn(acento_rojo),
            run_time=1.0
        )
        
        e = etiqueta("Efecto temprano", pos=RIGHT*3.5 + DOWN*1.5, color=ORANGE, font_size=40, ancho_max=5.5)
        self.play(FadeIn(e))
        
        self.wait(3.5)