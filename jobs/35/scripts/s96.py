from manim import *
from zenn_rig import *

class S96(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.3+LEFT*3.8, 
            playera=PLAYERA_MORADA, 
            altura=2.4, 
            expresion='mente_explotada', 
            pose='de_pie'
        )
        
        self.play(FadeIn(prota, shift=UP))
        
        cerebro_graf = curva(pos=RIGHT*3.0+UP*0.2, ancho=4.8, alto=2.4, color=AZUL_MARINO, acento=RED)
        self.play(Create(cerebro_graf), run_time=1.5)
        
        c = callout(
            text="Tu conciencia se adapta", 
            color=ORANGE, 
            pos=RIGHT*3.2+UP*1.9
        )
        self.play(FadeIn(c, shift=DOWN))
        
        cambiar_cara(prota, 'sorpresa')
        self.wait(3.0)
        
        lupa_obj = lupa(pos=RIGHT*2.2+DOWN*1.5, escala=1.1, color=INK)
        self.play(FadeIn(lupa_obj, shift=LEFT), run_time=1.0)
        
        self.wait(4.0)
        
        self.play(
            FadeOut(prota), 
            FadeOut(cerebro_graf), 
            FadeOut(c), 
            FadeOut(lupa_obj), 
            run_time=1.0
        )