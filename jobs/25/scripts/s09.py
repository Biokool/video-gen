from manim import *
from zenn_rig import *

class S09(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=42, seed=7, color=WHITE))

        protagonista_obj = protagonista(pos=(-3, -1, 0), playera=PLAYERA_AZUL, expresion='sorpresa', pose='de_pie')
        
        # El ojo_grande no es un objeto que se pueda instanciar y luego mover/transformar de forma independiente
        # si se quiere simular el ojo del protagonista, este ya está incluido en el objeto 'protagonista_obj'
        # y su expresión se controla mediante el parámetro 'expresion'.
        # Si se quisiera un ojo separado, se debería usar la función 'ojo_grande' y posicionarlo correctamente,
        # pero no tiene sentido añadirlo si ya el protagonista tiene ojos.
        # Por lo tanto, se elimina la creación y manipulación de 'ojo_grande_obj'.

        # Las exclamaciones deben crearse como objetos de texto de Manim, no con Tex de forma genérica
        # ya que Tex no está permitido según las restricciones.
        exclamacion_1 = Text("!", color=YELLOW).scale(3)
        exclamacion_2 = Text("!", color=YELLOW).scale(3)
        exclamacion_3 = Text("!", color=YELLOW).scale(3)

        exclamaciones = VGroup(exclamacion_1, exclamacion_2, exclamacion_3).arrange(RIGHT, buff=0.5)
        exclamaciones.next_to(protagonista_obj, RIGHT, buff=1.5)
        exclamaciones.shift(UP * 0.5)

        self.play(FadeIn(protagonista_obj))
        self.play(Write(exclamaciones))
        self.wait(1)

        callout_obj = callout("¡Increíble, verdad?", color=ORANGE, font_size=96)
        callout_obj.to_edge(UP)
        self.play(FadeIn(callout_obj))

        self.play(
            protagonista_obj.animate.shift(RIGHT * 0.5),
            exclamaciones.animate.shift(RIGHT * 0.5),
            FadeOut(callout_obj, shift=UP)
        )

        self.wait(1)
        self.play(
            FadeOut(protagonista_obj),
            FadeOut(exclamaciones)
        )
        self.wait(0.5)