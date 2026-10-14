from manim import *
from zenn_rig import *

class S21(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        # Título seguro superior y protagonista abajo
        titulo = banda_titulo("ASIMETRÍA CEREBRAL")
        self.play(
            FadeIn(titulo),
            run_time=0.5
        )
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_TEAL,
            altura=2.6,
            expresion='alegria_pura',
            pose='de_pie'
        )
        self.play(FadeIn(prota), run_time=0.8)
        
        # Props complementarios con color en el lado derecho
        corazon = moneda_dorada('♥', pos=RIGHT*3.2 + DOWN*1.3, radio=0.6)
        huella = hueso(pos=RIGHT*5.2 + DOWN*1.3, escala=0.8)
        
        self.play(
            Create(corazon),
            FadeIn(huella),
            run_time=1.0
        )
        
        # Animación de cambio de expresión para dinamismo
        cambiar_cara(prota, 'feliz')
        self.wait(5.0)
        
        self.play(
            FadeOut(prota),
            FadeOut(corazon),
            FadeOut(huella),
            FadeOut(titulo),
            run_time=0.5
        )