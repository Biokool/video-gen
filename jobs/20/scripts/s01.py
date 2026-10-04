from manim import *
from zenn_rig import *

class S01(Scene):
    def construct(self):
        # Tarjeta de canal "El Porqué"
        tarjeta = tarjeta_canal()
        self.play(Create(tarjeta), run_time=1.5)
        self.wait(1)

        # Personaje principal: El Porqué (protagonista)
        prota = protagonista(playera=PLAYERA_NARANJA, expresion='feliz', pose='de_pie')
        
        # Callout inicial "¡Hola!"
        hola_callout = callout("¡Hola!")

        # Transición: la tarjeta desaparece, el protagonista y el callout aparecen
        self.play(
            FadeOut(tarjeta),
            FadeIn(prota),
            FadeIn(hola_callout),
            run_time=1.5
        )
        self.wait(1) # El callout "¡Hola!" permanece brevemente

        # Desaparecer el callout
        self.play(FadeOut(hola_callout), run_time=1)
        
        # El protagonista permanece en pantalla para el resto de la narración
        self.wait(3)