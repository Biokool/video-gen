from manim import *
from zenn_rig import *

class S81(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        titulo = banda_titulo("LATERALIDAD Y MOVIMIENTO", color=TEAL)
        self.play(FadeIn(titulo))
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*3.8, 
            playera="teal", 
            altura=2.5, 
            expresion="mente_explotada", 
            pose="senalando"
        )
        self.play(Create(prota), run_time=1.0)
        
        ojo = ojo_grande(pos=RIGHT*3.5 + UP*0.3, escala=1.2, iris=TEAL)
        self.play(FadeIn(ojo), run_time=1.0)
        
        anotacion = etiqueta("¡Primeras patadas en el útero!", pos=RIGHT*3.4 + UP*1.8, color=ORANGE, font_size=40)
        self.play(FadeIn(anotacion), run_time=1.0)
        
        cambiar_cara(prota, "alegria_pura")
        self.wait(6.5)
        
        self.play(
            FadeOut(prota),
            FadeOut(ojo),
            FadeOut(anotacion),
            FadeOut(titulo),
            run_time=0.8
        )