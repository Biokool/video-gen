from manim import *
from zenn_rig import *

class S60(Scene):
    def construct(self):
        # Protagonista pensando (expresión analítica, playera verde)
        prota = protagonista(
            pos=LEFT * 4.2 + DOWN * 0.4,
            playera="verde",
            altura=3.0,
            expresion='pensando',
            pose='de_pie'
        )

        # Ojo grande que representa la visión
        ojo = ojo_grande(pos=RIGHT * 4.6 + UP * 1.6, escala=0.8)

        # Gráfica de agudeza visual con pico claro
        grafica = curva(pos=RIGHT * 1.6 + DOWN * 0.2, ancho=4.8, alto=2.6)

        # Entrada de elementos
        self.play(FadeIn(prota, scale=0.9), run_time=0.8)
        self.play(FadeIn(ojo), Create(grafica), run_time=1.7)
        self.wait(0.5)

        # Etiqueta que resalta el pico
        pico = etiqueta("Máxima a pocos metros", (1.4, 2.2))
        self.play(FadeIn(pico), run_time=0.8)

        # Pequeña animación de cambio de expresión para reacción
        self.wait(0.4)
        cambiar_cara(prota, 'sorpresa')
        self.wait(1.0)