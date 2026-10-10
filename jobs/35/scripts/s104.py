from manim import *
from zenn_rig import *

class S104(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        titulo = banda_titulo("¡SUSCRÍBETE Y DALE LIKE!", color=ORANGE)
        self.play(FadeIn(titulo))
        
        prota = protagonista(
            pos=DOWN*1.3+LEFT*3.2,
            playera=PLAYERA_TEAL,
            altura=2.4,
            expresion="alegria_pura",
            pose="senalando"
        )
        self.play(FadeIn(prota), run_time=1.0)
        
        et = etiqueta("¡No te pierdas nada!", pos=RIGHT*3.2+UP*0.5, color=INK)
        self.play(FadeIn(et), run_time=0.8)
        
        m = moneda_dorada(texto="$", pos=RIGHT*3.2+DOWN*1.2, radio=0.9)
        self.play(Create(m), run_time=1.0)
        
        cambiar_cara(prota, "euforico")
        self.wait(3.0)
        
        self.play(
            FadeOut(prota),
            FadeOut(et),
            FadeOut(m),
            FadeOut(titulo),
            run_time=0.8
        )