from manim import *
from zenn_rig import *

class S42(Scene):
    def construct(self):
        # Fondo espacial oscuro
        self.add(fondo(INK))

        # Protagonista (EL PORQUÉ) con playera amarilla, asombrado
        prota = protagonista(pos=LEFT * 4, playera='amarilla', expresion='sorpresa')
        self.play(FadeIn(prota))

        # Ojo gigante que simboliza la percepción
        ojo = ojo_grande(pos=RIGHT * 3 + UP * 1.5, escala=0.8, iris=TEAL)
        self.play(FadeIn(ojo))

        # La Tierra aparece en el centro
        tierra = planeta(pos=ORIGIN, radio=1.4, color=BLUE)
        self.play(Create(tierra), run_time=1)
        self.wait(0.5)

        # La Tierra se aleja y encoge mientras se revela el espacio con estrellas
        self.play(
            tierra.animate.scale(0.5).shift(RIGHT * 3.5),
            FadeIn(estrellas(n=42, seed=7, color=WHITE)),
            run_time=2
        )

        # Reacción de asombro extremo
        cambiar_cara(prota, 'mente_explotada')
        self.wait(1)