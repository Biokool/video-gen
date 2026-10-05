from manim import *
from zenn_rig import *

class S56(Scene):
    def construct(self):
        # Protagonista: posición con coordenada Z explícita (evita error de broadcasting)
        prota = protagonista(pos=(-3.2, -0.8, 0), playera=PLAYERA_NARANJA, expresion='normal')

        # Ojo grande: también con Z
        ojo = ojo_grande(pos=(-1.7, 0.7, 0), iris=TEAL)

        # Mapa mental: punto central + conexiones
        centro = Dot((2.2, 1.2, 0), radius=0.16, color=INK)
        extremos = [
            Dot((3.7, 2.3, 0), color=DARK_BLUE),
            Dot((3.9, -0.1, 0), color=DARK_BLUE),
            Dot((1.4, 2.7, 0), color=DARK_BLUE),
            Dot((0.9, 0.3, 0), color=DARK_BLUE),
        ]
        conexiones = [arrow(centro.get_center(), e.get_center(), color=GREY, width=4) for e in extremos]
        mapa = VGroup(centro, *extremos, *conexiones)

        # Entrada de personaje y ojo
        self.play(FadeIn(prota), FadeIn(ojo))
        self.wait(0.4)

        # Construcción del mapa mental (cerebro organizando ideas)
        self.play(
            *[Create(c) for c in conexiones],
            Write(centro),
            *[Create(e) for e in extremos],
            run_time=1.8
        )
        self.wait(0.3)

        # Cambio a expresión confundida
        cambiar_cara(prota, 'confundido')
        self.wait(0.3)

        # Callout corto (la narración explica el resto)
        truco = callout("El truco", color=ORANGE, font_size=48)
        truco.move_to(UP * 2.8)
        self.play(FadeIn(truco))
        self.wait(1.5)