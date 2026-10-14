from manim import *
from zenn_rig import *

class S17(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        titulo = banda_titulo("McManus, I. C. (2002). Harvard University Press", color=TEAL)
        self.play(
            FadeIn(titulo),
            run_time=0.5
        )
        
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.5,
            playera=PLAYERA_ROJA,
            altura=2.5,
            expresion="alegria_pura",
            pose="senalando"
        )
        self.play(FadeIn(prota), run_time=1.0)
        
        c = caja(etiqueta="Libro Clásico", pos=RIGHT * 3.2 + UP * 0.2, width=3.0)
        self.play(Create(c), run_time=1.0)
        
        txt_ref = etiqueta("Right Hand, Left Hand", pos=RIGHT * 3.2 + UP * 0.2, color=INK, font_size=32)
        self.play(Write(txt_ref), run_time=1.0)
        
        cambiar_cara(prota, "feliz")
        
        self.wait(2.0)
        
        self.play(
            FadeOut(prota),
            FadeOut(c),
            FadeOut(txt_ref),
            FadeOut(titulo),
            run_time=0.5
        )