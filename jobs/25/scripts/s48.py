from manim import *
from zenn_rig import *

class S48(Scene):
    def construct(self):
        # Protagonista con playera amarilla: la vista no basta
        prota = protagonista(
            LEFT * 3 + DOWN * 0.5,
            playera=PLAYERA_AMARILLA,
            altura=3.0,
            expresion="pensando",
            pose="senalando"
        )
        ojo = ojo_grande(RIGHT * 3.2 + UP * 0.4, escala=1.3, iris=TEAL)

        # Conceptos que el cerebro no puede procesar con la vista
        etiq_tam = etiqueta("TAMAÑO", (0.2, 2.2))
        etiq_temp = etiqueta("TEMPERATURA", (0.2, 0.5))
        etiq_comp = etiqueta("COMPOSICIÓN", (0.2, -1.2))

        # Entrada de personaje y ojo
        self.play(FadeIn(prota, shift=UP * 0.4), run_time=1.0)
        self.play(FadeIn(ojo, shift=DOWN * 0.3), run_time=1.0)
        self.wait(0.5)

        # Aparecen los datos que la vista no alcanza a procesar
        self.play(FadeIn(etiq_tam, shift=DOWN * 0.2), run_time=0.6)
        self.play(FadeIn(etiq_temp, shift=DOWN * 0.2), run_time=0.6)
        self.play(FadeIn(etiq_comp, shift=DOWN * 0.2), run_time=0.6)

        # Expresión de limitación: confundido / frustrado
        cambiar_cara(prota, "confundido")
        self.wait(0.4)

        # Los conceptos se desvanecen: la vista no puede con ellos
        self.play(
            FadeOut(etiq_tam),
            FadeOut(etiq_temp),
            FadeOut(etiq_comp),
            run_time=1.2
        )
        cambiar_cara(prota, "triste")
        self.wait(0.7)