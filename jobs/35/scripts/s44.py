from manim import *
from zenn_rig import *

class S44(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=35, seed=42, color=WHITE))
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera=PLAYERA_TEAL, 
            altura=2.4, 
            expresion='mente_explotada', 
            pose='senalando'
        )
        
        celestiales = VGroup(
            planeta(pos=RIGHT*3.2 + UP*0.5, radio=1.2, color=TEAL),
            adn(pos=RIGHT*2.5 + DOWN*1.5, escala=0.8, color=WHITE),
            fuego(pos=RIGHT*4.2 + DOWN*1.5, escala=0.8)
        )
        
        dato = callout(
            "¡Movimiento fetal\ndefine la lateralidad!", 
            color=ORANGE, 
            pos=RIGHT*3.2 + UP*1.8
        )
        
        self.play(
            FadeIn(prota),
            FadeIn(celestiales),
            FadeIn(dato),
            run_time=1.5
        )
        
        self.play(
            celestiales.animate.shift(UP*0.3),
            run_time=2.0,
            rate_func=there_and_back
        )
        
        cambiar_cara(prota, 'alegria_pura')
        self.wait(3.5)
        
        self.play(
            FadeOut(prota),
            FadeOut(celestiales),
            FadeOut(dato),
            run_time=1.0
        )