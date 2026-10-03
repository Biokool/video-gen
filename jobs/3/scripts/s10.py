from manim import *
from zenn_rig import * # Asegúrate de que zenn_rig.py esté en el mismo directorio o en PYTHONPATH

class S10(Scene):
    def construct(self):
        # Monigote inicial, posicionado a la izquierda.
        zenn = stick_idle(LEFT * 3)
        self.add(zenn) # Añadimos el monigote a la escena.

        # VO: "¿Por qué, si es tan masiva, no la vemos?"
        # Zenn levanta la mano y señala hacia arriba, como cuestionando algo invisible.
        # Problema: stick_point probablemente devuelve un Mobject (la nueva pose del monigote),
        # no una animación. self.play() espera objetos de animación.
        # Solución: Usar Transform para animar el cambio de la pose actual de 'zenn'
        # a la nueva pose devuelta por 'stick_point'.
        # Es importante pasar zenn.copy() a stick_point para que retorne un nuevo Mobject
        # que sirva como destino para la transformación, sin modificar zenn prematuramente.
        zenn_pointing_up = stick_point(zenn.copy(), zenn.get_center() + UP * 2)
        self.play(Transform(zenn, zenn_pointing_up))
        self.wait(2)

        # VO: "La respuesta es simple: la materia oscura no emite, absorbe ni refleja luz electromagnética."
        # Aparece un callout "INVISIBLE" para enfatizar su naturaleza.
        invisible_text = callout("INVISIBLE", color=TEAL).shift(UP * 2)
        self.play(FadeIn(invisible_text))
        self.wait(2.5)
        self.play(FadeOut(invisible_text))

        # VO: "Es como si fuera un fantasma que pasa a través de tus dedos sin dejar rastro."
        # Zenn señala hacia adelante, y una partícula tenue ("fantasma") pasa a través de él.
        # Aplicamos la misma corrección aquí.
        zenn_pointing_right = stick_point(zenn.copy(), zenn.get_center() + RIGHT * 2)
        self.play(Transform(zenn, zenn_pointing_right))
        self.wait(0.5)

        # Representamos la "partícula fantasma" como un punto tenue.
        # CORRECCIÓN: El error indica que 'opacity' no es un argumento válido para Mobject.__init__().
        # Para `Dot` (que es un VMobject), la opacidad del relleno se controla con 'fill_opacity'.
        ghost_particle = Dot(point=RIGHT * 5, radius=0.2, color=INK, fill_opacity=0.3)
        self.play(Create(ghost_particle))
        # La partícula se mueve rápidamente a través de zenn, de derecha a izquierda.
        self.play(ghost_particle.animate.shift(LEFT * 10), run_time=2)
        self.play(FadeOut(ghost_particle))

        # Pausa final tras la analogía.
        self.wait(1.5)