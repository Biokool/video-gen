from manim import *
from zenn_rig import *

class S29(Scene):
    def construct(self):
        # Protagonista con playera rosa, sorprendido y señalando
        prota = protagonista(
            pos=[-4.0, -0.8, 0],
            playera="rosa",
            altura=3.0,
            expresion="sorpresa",
            pose="senalando"
        )
        self.play(FadeIn(prota, run_time=1.0))

        # Ojo grande: lo que vemos es solo la superficie
        ojo = ojo_grande(pos=[4.6, 2.6, 0], escala=0.8, iris=TEAL)
        self.play(Create(ojo, run_time=1.0))

        # Sólido aparente: una caja con etiqueta "mesa"
        mesa = caja("mesa", pos=[2.2, -0.2, 0], width=1.5)
        self.play(Create(mesa, run_time=1.0))
        self.wait(0.5)

        # Formas microscópicas: célula, molécula y átomo
        celula = VGroup(
            Circle(radius=0.7, color=ORANGE, fill_opacity=0.4),
            Circle(radius=0.3, color=RED, fill_opacity=0.6)
        ).move_to([0.4, -0.6, 0])

        linea = Line([2.4, -0.6, 0], [3.6, -0.6, 0], color=INK)
        bola1 = Circle(radius=0.35, color=BLUE, fill_opacity=0.6).move_to([2.4, -0.6, 0])
        bola2 = Circle(radius=0.35, color=GREEN, fill_opacity=0.6).move_to([3.6, -0.6, 0])
        molecula = VGroup(linea, bola1, bola2)

        electrones = VGroup(
            Ellipse(width=1.2, height=0.3, color=TEAL).rotate(0.5),
            Ellipse(width=1.2, height=0.3, color=TEAL).rotate(-0.8),
        ).move_to([5.0, -0.6, 0])
        nucleo = Circle(radius=0.2, color=RED, fill_opacity=0.8).move_to([5.0, -0.6, 0])
        atomo = VGroup(nucleo, electrones)

        micro = VGroup(celula, molecula, atomo)
        self.play(
            FadeOut(mesa),
            FadeIn(micro, run_time=1.5)
        )

        # Momento de asombro: aplicar el cambio de cara y esperar
        cambiar_cara(prota, "mente_explotada")
        self.wait(2.5)