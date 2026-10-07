from manim import *
from zenn_rig import *

class S01(Scene):
    def construct(self):
        # Fondo de papel cálido estilo divulgación
        self.add(fondo_papel())
        
        # Elementos principales
        tarjeta = tarjeta_canal(texto="EL PORQUÉ", subtitulo="curiosidad científica")
        tarjeta.shift(LEFT * 1.5 + UP * 0.2)
        
        prota = protagonista(
            pos=RIGHT * 5.0 + DOWN * 1.2, 
            playera=PLAYERA_NARANJA, 
            altura=2.5, 
            expresion='feliz', 
            pose='de_pie'
        )
        
        # Objetos temáticos flotando alrededor del protagonista
        prop_planeta = planeta(pos=RIGHT * 4.5 + UP * 1.5, radio=0.6, color=TEAL)
        prop_lupa = lupa(pos=RIGHT * 2.0 + UP * 1.8, escala=0.7)
        
        # Secuencia de Animación
        # 1. Aparece la tarjeta de presentación del canal
        self.play(FadeIn(tarjeta, shift=RIGHT * 0.5), run_time=1.5)
        self.wait(0.5)
        
        # 2. El protagonista entra en escena deslizándose
        self.play(prota.animate.shift(LEFT * 1.8), run_time=1.5)
        
        # 3. Aparecen los objetos de curiosidad y el protagonista se alegra
        self.play(
            FadeIn(prop_planeta, scale=0.5),
            FadeIn(prop_lupa, scale=0.5),
            Transform(prota, cambiar_cara(prota, 'alegria_pura')),
            run_time=1.5
        )
        
        # 4. Pausa final para completar el tiempo de narración (~9 segundos en total)
        self.wait(4.0)