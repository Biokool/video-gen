from manim import *
from zenn_rig import *

class S01(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        tc = tarjeta_canal(texto="EL PORQUÉ", subtitulo="curiosidad científica")
        self.play(FadeIn(tc, shift=UP), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(tc, shift=DOWN), run_time=1.0)
        
        prota = protagonista(
            pos=DOWN*1.5 + LEFT*3.5,
            playera=PLAYERA_NARANJA,
            altura=2.5,
            expresion="sorpresa",
            pose="senalando"
        )
        
        et = etiqueta(
            texto="¿Por qué usas más una mano?",
            pos=RIGHT*3.2 + UP*1.0,
            color=ORANGE
        )
        
        self.play(FadeIn(prota, shift=RIGHT), Create(et), run_time=1.5)
        self.wait(2.5)
        
        cambiar_cara(prota, "alegria_pura")
        self.wait(2.0)
        
        self.play(FadeOut(prota), FadeOut(et), run_time=1.0)
        self.wait(0.5)