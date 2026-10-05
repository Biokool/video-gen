from manim import *
from zenn_rig import *

class S66(Scene):
    def construct(self):
        # Fondo cósmico
        self.add(fondo(INK))
        estrellas_d = estrellas(n=42, seed=7, color=WHITE)
        self.play(FadeIn(estrellas_d), run_time=1.0)
        self.wait(0.5)

        # El Porqué con playera verde, expresión de asombro
        prota = protagonista(
            pos=LEFT * 3 + DOWN * 0.5,
            playera=PLAYERA_VERDE,
            altura=2.8,
            expresion='sorpresa',
            pose='de_pie'
        )
        self.play(FadeIn(prota, shift=UP * 0.4), run_time=1.0)

        # Ojo grande que observa
        ojo = ojo_grande(
            pos=RIGHT * 3.2 + UP * 0.8,
            escala=1.0,
            iris=YELLOW
        )
        self.play(FadeIn(ojo, shift=DOWN * 0.3), run_time=1.0)

        # Rayo de luz cósmica
        rayo = arrow(
            start=RIGHT * 6 + UP * 2.2,
            end=LEFT * 5.5 + DOWN * 1.8,
            color=YELLOW,
            width=6
        )
        self.play(Create(rayo), run_time=1.8)
        self.wait(0.3)

        # Mota de polvo en el rayo
        polvo = sol(
            pos=LEFT * 1.2 + UP * 0.6,
            radius=0.12,
            color=YELLOW
        )
        self.play(FadeIn(polvo), run_time=1.0)
        self.play(Create(red_accent(polvo, scale=1.8)), run_time=0.6)

        # El Porqué mira con más sorpresa
        cambiar_cara(prota, 'mente_explotada')
        self.wait(1.2)