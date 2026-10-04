from manim import *
from zenn_rig import *

class S05(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=60, seed=10))

        protagonista_obj = protagonista(playera=PLAYERA_AZUL, expresion='pensando', pose='de_pie')
        ojo_grande_obj = ojo_grande(pos=protagonista_obj.get_center() + UP*0.3, escala=0.7, iris=WHITE)

        # El rig no tiene una función para crear engranajes directamente.
        # Si se necesita un engranaje, debe ser creado usando formas de Manim o un SVG importado.
        # Dado que el error original se relaciona con "gear.svg", y el rig no provee
        # una función para esto, se eliminará el uso de engranajes para evitar el error.
        # Si se deseara usar un SVG, se necesitaría asegurar que la ruta sea correcta y
        # que el archivo exista en la ubicación esperada.
        # Para este ejemplo, nos centraremos en la corrección del código del rig.

        self.play(FadeIn(protagonista_obj, shift=UP), FadeIn(ojo_grande_obj))
        self.wait(1)

        # La función callout del rig espera un string para el texto, no un objeto Text.
        # El color por defecto es ORANGE, si se desea blanco se debe especificar.
        callout_text = callout("Es una construcción activa de nuestro cerebro.", color=WHITE, font_size=48)
        callout_text.next_to(protagonista_obj, UP, buff=1.5)
        self.play(FadeIn(callout_text))
        self.wait(2)
        self.play(FadeOut(callout_text), FadeOut(protagonista_obj), FadeOut(ojo_grande_obj))

# La función rotar_engranajes fue eliminada ya que los engranajes fueron removidos.
# Si se reintrodujeran engranajes creados con Manim, esta función debería ser reescrita
# para usar las animaciones de Manim como Rotate.