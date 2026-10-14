from manim import *
from zenn_rig import *

class S23(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*3.8,
            playera=PLAYERA_AMARILLA,
            altura=2.5,
            expresion='pensando',
            pose='de_pie'
        )
        
        titulo = banda_titulo("¿Proceso gradual o repentino?", color=MOSTAZA)
        
        caja_bloque = caja(etiqueta="BLOQUE", pos=RIGHT*3.5 + UP*0.2, width=2.0)
        
        flechita = arrow(
            start=RIGHT*1.2 + UP*0.2,
            end=RIGHT*2.3 + UP*0.2,
            color=INK,
            width=8
        )
        
        etiqueta_secundaria = etiqueta("¿Hemisferio dominante?", pos=RIGHT*3.2 + DOWN*1.5, color=CORAL, font_size=40)
        
        self.play(
            FadeIn(titulo),
            FadeIn(prota),
            FadeIn(caja_bloque),
            run_time=1.0
        )
        
        self.play(
            Create(flechita),
            FadeIn(etiqueta_secundaria),
            run_time=1.5
        )
        
        cambiar_cara(prota, 'sorpresa')
        self.play(
            prota.animate.shift(RIGHT*0.5),
            run_time=1.5
        )
        
        self.wait(5.0)