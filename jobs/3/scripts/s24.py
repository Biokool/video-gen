from manim import *
from zenn_rig import *

class S24(Scene):
    def construct(self):
        # Fondo espacial
        self.add(fondo(INK), estrellas())

        # Monigote pensativo y el planeta "puzzle"
        stick = stick_idle(pos=LEFT * 3.5, color=WHITE)
        puzzle_planet = planeta(pos=RIGHT * 3.5, color=TEAL, radio=1.2)

        # Entrada de los elementos principales
        self.play(FadeIn(stick), Create(puzzle_planet))

        # Añadir la expresión 'preocupado' al monigote
        # La función 'expresion' devuelve un Mobject, no una animación.
        # Necesitamos animar la aparición de ese Mobject.
        preocupado_expr = expresion(stick, tipo='preocupado')
        self.play(Create(preocupado_expr))
        self.wait(0.5)

        # Primer callout: "Medio siglo buscando..."
        callout_1 = callout("Medio siglo buscando...", font_size=72).next_to(stick, UP)
        self.play(Write(callout_1))
        self.wait(1.5)
        self.play(FadeOut(callout_1))

        # Monigote piensa sobre la "pieza cósmica"
        # La función 'stick_think' devuelve un Mobject (la burbuja de pensamiento),
        # no una animación. Necesitamos animar su aparición.
        # También, al aparecer la burbuja de pensamiento, la expresión anterior
        # (preocupado) debería desaparecer.
        thinking_bubble_mobject = stick_think(stick, text="¿El Gran Puzzle?")
        self.play(FadeOut(preocupado_expr), Create(thinking_bubble_mobject))
        self.wait(2)

        # Segundo callout: "...pieza clave del cosmos" cerca del planeta
        callout_2 = callout("...pieza clave del cosmos", font_size=72).next_to(puzzle_planet, UP)
        self.play(Write(callout_2))
        self.wait(1.5)

        # Tercer callout (transformación del segundo): "...diseñada para no ser encontrada."
        # Al transformar el callout, también desvanecemos la burbuja de pensamiento.
        callout_3 = callout("...dise\xF1ada para no ser encontrada.", font_size=72).next_to(stick, UP)
        self.play(Transform(callout_2, callout_3), FadeOut(thinking_bubble_mobject))
        self.wait(2.5)

        # Salida de la escena
        # callout_2 ahora contiene el Mobject de callout_3 debido a la transformación.
        self.play(FadeOut(stick), FadeOut(puzzle_planet), FadeOut(callout_2))
        self.wait(0.5)