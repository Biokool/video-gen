from manim import *
from zenn_rig import *

class S07(Scene):
    def construct(self):
        # Fondo nocturno (color negro)
        self.add(fondo(INK))

        # Título superior (banda)
        titulo = banda_titulo(
            "PICO 1 – Tu cuerpo cree que sigue de día",
            color=YELLOW,
        )
        self.play(FadeIn(titulo, shift=DOWN))
        self.wait(0.5)

        # Protagonista azul, posición izquierda inferior y altura adecuada
        prota = version_prota(
            2,                              # versión azul
            pos=DOWN * 1.2 + LEFT * 3.5,    # y <= -1.2, x a la izquierda
            altura=2.6,                     # ≤ 2.6 para que la banda no lo tape
        )
        self.play(FadeIn(prota, shift=UP))
        self.wait(0.5)

        # Cambiar expresión a "pensando"
        # cambiar_cara devuelve un VGroup con la nueva cara → usamos Transform
        nueva_cara = cambiar_cara(prota, "pensando")
        self.play(Transform(prota, nueva_cara))
        self.wait(0.3)

        # Reloj de arena (usamos reloj de pared como sustituto)
        timer = reloj_pared(
            radius=1.0,
            pos=DOWN * 1.2 + RIGHT * 3.5,
            hora_3=True,
        )
        self.play(FadeIn(timer, shift=UP))
        self.wait(0.3)

        # Etiqueta con el dato "90 min"
        dato = etiqueta(
            "90 min",
            (DOWN * 1.2 + RIGHT * 3.5 + UP * 0.9),
            color=YELLOW,
            font_size=40,
        )
        self.play(FadeIn(dato, shift=UP))
        self.wait(0.2)

        # Flecha del protagonista al reloj
        flecha = arrow(
            start=prota.get_center(),
            end=timer.get_center(),
            color=INK,
            width=8,
        )
        self.play(FadeIn(flecha))
        self.wait(0.2)

        # Acento rojo sobre el reloj
        accent = red_accent(timer, scale=1.3)
        self.play(FadeIn(accent))
        self.wait(2.0)

        # Salida
        self.play(FadeOut(VGroup(titulo, prota, timer, dato, flecha, accent)))