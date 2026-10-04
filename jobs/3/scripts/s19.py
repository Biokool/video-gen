from manim import *
from zenn_rig import *

class S19(Scene):
    def construct(self):
        # VOZ: Algunos científicos proponen que quizás no sea una partícula,
        # sino que nuestra comprensión de la gravedad es incompleta.
        scientists = stick_group(3, center=LEFT * 3, spacing=1.6, color=INK)
        self.add(scientists)
        self.wait(0.5)

        thought_bubble = stick_think(scientists[1], "Gravedad Incompleta?")
        self.play(Create(thought_bubble))
        self.wait(2.5)
        self.play(FadeOut(thought_bubble))

        # VOZ: Teorías como la Dinámica Newtoniana Modificada (MOND)
        # intentan explicar las curvas de rotación sin materia oscura.
        mond_fig = stick_idle(pos=LEFT * 3, color=INK)
        # El error "Unexpected argument Circle passed to Scene.play()"
        # ocurre porque Transform no puede manejar directamente la transformación
        # de un VGroup de 3 figuras (scientists) a una única figura (mond_fig)
        # debido a la diferencia en la estructura de los Mobjects.
        # La solución es usar FadeOut y FadeIn para el cambio.
        self.play(
            FadeOut(scientists, run_time=1),
            FadeIn(mond_fig, run_time=1)
        )
        self.wait(0.5)

        mond_text = callout("MOND", color=ORANGE).next_to(mond_fig, UP * 2)
        self.play(FadeIn(mond_text, shift=UP))
        self.wait(1)

        rotation_curve = curva(pos=RIGHT * 2.5, ancho=5.2, alto=2.8, color=INK, acento=INK)
        self.play(Create(rotation_curve))
        self.wait(0.5)

        # CORRECCIÓN: La función `stick_point` devuelve un Mobject (la figura en pose de apuntar),
        # no una animación. Pasar un Mobject directamente a `self.play()` causa el error `TypeError`.
        # Para animar el cambio de `mond_fig` a su versión apuntando, usamos `Transform`.
        pointing_mond_fig = stick_point(mond_fig, rotation_curve.get_center())
        self.play(Transform(mond_fig, pointing_mond_fig))
        self.wait(3)

        # VOZ: Sin embargo, MOND falla al explicar la radiación del fondo cósmico de microondas
        # y las lentes gravitacionales a gran escala.
        expresion_preocupado = expresion(mond_fig, tipo='preocupado')
        self.play(FadeIn(expresion_preocupado))
        self.wait(0.5)

        failure_1_text = callout("Fondo Cósmico?", color=YELLOW).next_to(rotation_curve, UP)
        failure_2_text = callout("Lentes Gravitacionales?", color=YELLOW).next_to(rotation_curve, DOWN)

        self.play(
            FadeIn(failure_1_text, shift=UP),
            FadeIn(failure_2_text, shift=DOWN)
        )
        self.wait(1.5)

        accent_curve = red_accent(rotation_curve)
        self.play(Create(accent_curve))
        self.wait(2.5)

        self.play(
            FadeOut(mond_fig),
            FadeOut(mond_text),
            FadeOut(rotation_curve),
            FadeOut(expresion_preocupado),
            FadeOut(failure_1_text),
            FadeOut(failure_2_text),
            FadeOut(accent_curve)
        )
        self.wait(0.5)