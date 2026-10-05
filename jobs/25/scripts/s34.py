from manim import *
from zenn_rig import *

class S34(Scene):
    def construct(self):
        # Personaje principal con playera rosa, observando
        prota = version_prota(7, pos=LEFT * 3.5, altura=3.0)
        cambiar_cara(prota, 'pensando')

        # Ojo gigante que enfatiza "ves"
        ojo = ojo_grande(pos=RIGHT * 2.8 + UP * 1.2, escala=1.2)

        # Procesos: matraz burbujeante + fuego
        matraz_proceso = matraz(pos=RIGHT * 2.6 + DOWN * 1.2, escala=0.9, liquido=TEAL)
        fue = fuego(pos=RIGHT * 2.7 + DOWN * 2.2, escala=0.8)

        self.play(FadeIn(prota), FadeIn(ojo), FadeIn(matraz_proceso), FadeIn(fue))
        self.wait(0.5)

        # Animación de procesos: pulso del matraz y parpadeo del fuego
        self.play(matraz_proceso.animate.scale(1.15), fue.animate.scale(1.2), run_time=1.2)
        self.play(matraz_proceso.animate.scale(1 / 1.15), fue.animate.scale(1 / 1.2), run_time=1.2)

        # El protagonista señala suavemente el proceso
        self.play(prota.animate.shift(UP * 0.2), run_time=0.8)
        self.wait(0.3)