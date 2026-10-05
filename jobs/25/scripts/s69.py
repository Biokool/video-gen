from manim import *
from zenn_rig import *

class S69(Scene):
    def construct(self):
        # Protagonista reflexivo con playera amarilla (tema pregunta)
        prota = protagonista(
            LEFT * 2.8,
            playera=PLAYERA_AMARILLA,
            altura=3.0,
            expresion="pensando",
            pose="de_pie",
        )

        # Ojo gigante como símbolo de percepción / biología
        ojo = ojo_grande(RIGHT * 1.8, escala=1.1, iris=TEAL)

        # Etiquetas cortas: herramientas y biología
        etq_herramientas = etiqueta("herramientas", (-4.8, 2.0))
        etq_biologia = etiqueta("biología", (4.8, -1.8))

        # Entrada
        self.play(FadeIn(prota, shift=UP))
        self.play(Create(ojo), FadeIn(etq_herramientas), FadeIn(etq_biologia))

        # Pequeño movimiento: el protagonista se acerca ligeramente al ojo
        self.play(prota.animate.shift(RIGHT * 0.4), ojo.animate.scale(1.15))
        self.wait(1.5)

        # Reacción final: sigue pensando, el ojo pulsa
        cambiar_cara(prota, "confundido")
        self.play(ojo.animate.scale(0.95))
        self.wait(2)