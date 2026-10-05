from manim import *
from zenn_rig import *

class S58(Scene):
    def construct(self):
        # Montaña desproporcionadamente grande (curva estilizada)
        montana = curva(pos=RIGHT * 2.5 + DOWN * 0.2, ancho=6.4, alto=3.6, color=AZUL_MARINO, acento=RED)
        self.play(Create(montana), run_time=1.8)

        # Protagonista observando con asombro
        prota = protagonista(pos=LEFT * 2.8 + DOWN * 0.8, playera="naranja", altura=3.0, expresion="sorpresa", pose="de_pie")
        self.play(FadeIn(prota, shift=UP), run_time=1.2)

        # Ojo grande: percepción visual
        ojo = ojo_grande(pos=LEFT * 3.6 + UP * 1.4, escala=0.8, iris=TEAL)
        self.play(FadeIn(ojo, shift=RIGHT), run_time=1.0)

        # Reacción exagerada
        cambiar_cara(prota, "mente_explotada")
        self.wait(0.5)

        # Enfatizar la inmensidad
        self.play(montana.animate.scale(1.15), run_time=2.0)

        # Texto corto de apoyo
        etiqueta("INMENSO", (0, 2.6))
        self.wait(1.5)