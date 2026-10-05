from manim import *
from zenn_rig import *

class S72(Scene):
    def construct(self):
        # Protagonista (EL PORQUÉ) con expresión pensativa
        prota = protagonista(
            pos=LEFT * 3.2 + DOWN * 0.5,
            playera="naranja",
            altura=2.2,
            expresion='pensando',
            pose='de_pie'
        )
        self.play(FadeIn(prota))
        self.wait(0.4)

        # Ojo grande a la derecha (lo que ve el personaje)
        ojo = ojo_grande(pos=RIGHT * 3.6 + UP * 0.8, escala=1.0, iris=TEAL)
        self.play(FadeIn(ojo))
        self.wait(0.3)

        # Microscopio construido con formas simples (prop)
        base = Rectangle(width=1.6, height=0.15, fill_color=AZUL_MARINO,
                         fill_opacity=0.9, stroke_color=AZUL_MARINO)
        base.move_to(ORIGIN + DOWN * 1.2)
        brazo = Rectangle(width=0.15, height=1.8, fill_color=AZUL_MARINO,
                          fill_opacity=0.9, stroke_color=AZUL_MARINO)
        brazo.move_to(ORIGIN + LEFT * 0.4 + UP * 0.2)
        tubo = Rectangle(width=1.4, height=0.2, fill_color=CORAL,
                         fill_opacity=0.9, stroke_color=CORAL)
        tubo.move_to(ORIGIN + RIGHT * 0.5 + UP * 0.5)
        ocular = Rectangle(width=0.2, height=0.5, fill_color=INK,
                           fill_opacity=0.9, stroke_color=INK)
        ocular.move_to(ORIGIN + RIGHT * 1.3 + UP * 0.5)
        objetivo = Rectangle(width=0.15, height=0.7, fill_color=AZUL_MARINO,
                             fill_opacity=0.9, stroke_color=AZUL_MARINO)
        objetivo.move_to(ORIGIN + LEFT * 0.1 + UP * 0.1)
        tornillo = Circle(radius=0.1, fill_color=WHITE, fill_opacity=1,
                          stroke_color=INK)
        tornillo.move_to(ORIGIN + LEFT * 0.4 + UP * 0.6)

        microscopio = VGroup(base, brazo, tubo, ocular, objetivo, tornillo)
        microscopio.move_to(LEFT * 1.2 + DOWN * 0.3)
        self.play(Create(microscopio), run_time=1.2)
        self.wait(0.3)

        # El microscopio se alinea con el ojo (el ocular toca el ojo grande)
        self.play(
            microscopio.animate.move_to(RIGHT * 1.0 + DOWN * 0.3),
            run_time=1.5
        )
        # Cambio de expresión: ahora comprende
        cambiar_cara(prota, 'sorpresa')
        self.play(
            prota.animate.shift(UP * 0.1),
            run_time=0.3
        )
        self.wait(0.8)

        # Etiqueta corta (opcional, sin tapar nada)
        etiqueta("lente delante", (0, 2.8))
        self.wait(0.5)