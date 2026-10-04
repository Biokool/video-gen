from manim import *
from zenn_rig import *

class S13(Scene):
    def construct(self):
        # Fondo amarillo pálido
        self.add(fondo(YELLOW))

        # Título superior
        titulo = banda_titulo("Intuición vs Biología", color=ORANGE)
        self.add(titulo)

        # Stick que tropezará
        tropezador = stick_idle(pos=LEFT * 3, height=2.2, color=WHITE)
        self.play(FadeIn(tropezador, shift=RIGHT))
        self.wait(0.5)

        # Corrida que termina tropezando
        self.play(
            stick_run(
                tropezador,
                target=LEFT * 0.5,
                run_time=1.5,
                steps=10,
            )
        )
        self.wait(0.3)

        # Stick que escribe con dificultad
        escritor = stick_idle(pos=RIGHT * 3, height=2.2, color=WHITE)
        self.play(FadeIn(escritor, shift=LEFT))
        expresion(escritor, "preocupado")
        self.wait(0.5)

        # Callout con texto breve
        mensaje = callout("¡Es biología!", color=ORANGE, font_size=96).shift(UP * 2)
        self.play(FadeIn(mensaje, shift=DOWN))
        self.wait(0.3)

        # Flecha del escritor al mensaje
        flecha = arrow(escritor.get_center() + UP * 0.5, mensaje.get_center(), color=INK, width=8)
        self.play(FadeIn(flecha))
        self.wait(0.5)

        # Pequeña pausa final
        self.wait(1)