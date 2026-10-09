from manim import *
from zenn_rig import *

class S46(Scene):
    def construct(self):
        # 1. Configuración del fondo
        self.add(fondo(AZUL_MARINO))
        self.add(estrellas(n=30, seed=42, color=WHITE))
        
        # 2. Creación del protagonista (versión 8: teal/final)
        # Se ajusta la posición para dejar espacio al logo
        prota = version_prota(8, pos=LEFT*3.5 + DOWN*1.2, altura=2.6)
        self.play(FadeIn(prota, shift=UP*0.3), run_time=1.0)
        
        # 3. Elemento de Layout Principal
        # Se usa tarjeta_canal como elemento central. 
        # Según las instrucciones, no se debe mezclar con callout/banda_titulo en la misma escena.
        logo = tarjeta_canal(texto='EL PORQUÉ', subtitulo='curiosidad científica')
        logo.scale(0.8).move_to(RIGHT*2.2 + UP*0.5)
        self.play(FadeIn(logo, scale=0.9), run_time=1.2)
        
        self.wait(0.5)
        
        # 4. Animación del personaje
        # cambiar_cara actualiza el objeto prota internamente
        cambiar_cara(prota, 'euforico')
        self.play(
            prota.animate.scale(1.1).shift(RIGHT*0.2), 
            run_time=0.6
        )
        
        # 5. Texto secundario usando etiqueta()
        # Se usa etiqueta en lugar de callout para evitar conflictos de layout
        despedida = etiqueta(
            "¡Gracias por acompañarnos!", 
            pos=RIGHT*2.2 + DOWN*2.2, 
            color=YELLOW,
            font_size=42
        )
        self.play(FadeIn(despedida, shift=UP*0.2), run_time=0.8)
        
        self.wait(2.5)
        
        # 6. Cierre de la escena
        self.play(
            FadeOut(prota), 
            FadeOut(logo), 
            FadeOut(despedida), 
            run_time=1.0
        )
        
        self.wait(0.5)