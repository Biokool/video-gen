from manim import *
from zenn_rig import *

class S64(Scene):
    def construct(self):
        self.add(fondo(AZUL_MARINO))
        
        titulo = banda_titulo("TESTOSTERONA Y HEMISFERIO DERECHO", color=ORANGE)
        self.play(FadeIn(titulo), run_time=1.0)
        
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.8,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="mente_explotada",
            pose="senalando"
        )
        self.play(FadeIn(prota), run_time=1.0)
        
        c = curva(pos=RIGHT * 2.8 + UP * 0.2, ancho=5.0, alto=2.5, color=WHITE, acento=TEAL)
        self.play(Create(c), run_time=1.5)
        
        et = etiqueta("Mayor testosterona\n= hemisferio derecho", pos=RIGHT * 3.2 + UP * 1.5, color=WHITE, font_size=36, ancho_max=5.5)
        self.play(FadeIn(et), run_time=1.0)
        
        cambiar_cara(prota, "alegria_pura")
        self.wait(2.0)
        
        self.play(
            FadeOut(prota),
            FadeOut(c),
            FadeOut(et),
            FadeOut(titulo),
            run_time=1.0
        )