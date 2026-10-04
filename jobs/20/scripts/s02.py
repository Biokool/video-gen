from manim import *
from zenn_rig import *

class S02(Scene):
    def construct(self):
        # Protagonista: playera naranja, expresión de estrés/nerviosismo
        prota = protagonista(pos=LEFT * 3, playera=PLAYERA_NARANJA, expresion='nervioso', pose='de_pie')
        self.play(FadeIn(prota))

        # Nube de pensamientos caóticos (usando etiquetas)
        pensamiento_estres = etiqueta("Estrés", pos=UP * 1.8 + LEFT * 1.5, color=INK)
        pensamiento_tareas = etiqueta("Tareas", pos=UP * 2.5 + LEFT * 3.5, color=INK)
        pensamiento_caos = etiqueta("Caos", pos=UP * 0.8 + LEFT * 3.8, color=INK)
        pensamiento_pendientes = etiqueta("Pendientes", pos=UP * 0.5 + LEFT * 1.0, color=INK)
        
        # Botón de "RESET"
        boton_reset = callout("RESET", color=ORANGE).next_to(prota, RIGHT * 2 + UP * 0.5)

        # Animación de los pensamientos
        self.play(
            LaggedStart(
                FadeIn(pensamiento_estres),
                FadeIn(pensamiento_tareas),
                FadeIn(pensamiento_caos),
                FadeIn(pensamiento_pendientes),
                lag_ratio=0.3
            ),
            run_time=2
        )
        self.wait(0.5) 

        # Animación del botón de RESET
        self.play(Create(boton_reset))

        # Mantener la escena para la narración
        self.wait(3) 

        # Limpiar la escena
        self.play(
            FadeOut(prota),
            FadeOut(pensamiento_estres),
            FadeOut(pensamiento_tareas),
            FadeOut(pensamiento_caos),
            FadeOut(pensamiento_pendientes),
            FadeOut(boton_reset)
        )