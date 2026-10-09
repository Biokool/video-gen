from manim import *
from zenn_rig import *

class S43(Scene):
    def construct(self):
        # Fondo y Título Único (Solo se permite una banda/título por escena)
        self.add(fondo(CREMA))
        banda = banda_titulo("LA IMAGEN QUE REESCRIBIÓ LA HISTORIA", color=CORAL)
        self.play(FadeIn(banda, shift=DOWN * 0.4), run_time=0.6)

        # Protagonista en posición segura (abajo a la izquierda)
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.5, 
            playera="rosa", 
            altura=2.6, 
            expresion="sorpresa", 
            pose="senalando"
        )
        self.play(FadeIn(prota, shift=RIGHT * 0.5), run_time=0.8)

        # Elementos visuales (Caja y Personaje secundario)
        mapa = caja("ARQUEOLOGÍA", pos=RIGHT * 3.0 + DOWN * 0.5, width=1.8)
        opera = personaje(pos=RIGHT * 3.0 + UP * 1.5, cuerpo=CORAL, altura=2.2, expresion_tipo="sorpresa")
        
        self.play(FadeIn(mapa, scale=0.7), run_time=0.8)
        self.play(FadeIn(opera, scale=0.6, shift=UP * 0.4), run_time=1.0)

        self.wait(0.5)
        cambiar_cara(prota, "confundido")
        self.wait(0.5)

        # Usamos etiquetas en lugar de callouts para evitar el error de múltiples títulos
        etiq_1 = etiqueta(
            "Fantasía visual vs. excavación", 
            pos=RIGHT * 3.0 + UP * 3.0, 
            color=AZUL_MARINO, 
            font_size=36
        )
        self.play(Write(etiq_1), run_time=0.8)
        self.wait(1.5)

        # Transición de ideas
        self.play(
            FadeOut(etiq_1, shift=UP * 0.3),
            FadeOut(opera, scale=0.8),
            run_time=0.6
        )

        etiq_2 = etiqueta(
            "Una imagen > toda la evidencia", 
            pos=RIGHT * 3.0 + UP * 1.5, 
            color=RED, 
            font_size=42
        )
        self.play(FadeIn(etiq_2, scale=0.9), run_time=0.8)
        
        # Reacción final del protagonista
        cambiar_cara(prota, "mente_explotada")
        self.wait(2.0)

        # Limpieza final
        self.play(
            FadeOut(etiq_2),
            FadeOut(mapa),
            FadeOut(prota),
            FadeOut(banda),
            run_time=0.8
        )