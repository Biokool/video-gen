from manim import *
from zenn_rig import *

class S06(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=42, seed=7, color=WHITE))

        prota = protagonista(pos=(-3, 0, 0), playera=PLAYERA_AZUL, expresion='sorpresa', pose='de_pie')
        ojo = ojo_grande(pos=(-3, 0.5, 0), escala=0.7, iris=AZUL_MARINO)
        self.play(Create(prota), Create(ojo))

        linea_recta = Line(start=(-2, -1, 0), end=(2, -1, 0), color=WHITE)
        self.add(linea_recta)

        curva_drastica = curva(pos=(0, -1, 0), ancho=4.0, alto=1.5, color=WHITE, acento=RED)
        self.play(
            Transform(linea_recta, curva_drastica),
            cambiar_cara(prota, 'mente_explotada')
        )
        self.wait(1)

        callout_text = callout("¡La distancia lo cambia todo!", color=CORAL)
        self.play(FadeIn(callout_text))
        self.wait(2)