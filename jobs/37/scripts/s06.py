from manim import *
from zenn_rig import *

class S06(Scene):
    def construct(self):
        # Título principal (único por escena)
        title = banda_titulo("Cascos Vikingos", color=ORANGE)
        self.play(FadeIn(title, shift=UP))

        # Protagonista (versión 6: transmisión verde señalando)
        # Con banda_titulo arriba el protagonista debe estar bajo ella:
        #   y <= -1.2 y altura <= 2.6
        prota = version_prota(
            6,
            pos=DOWN * 1.2 + LEFT * 3.5,
            altura=2.6,          # altura ajustada para que la banda no tape la cabeza
        )
        self.play(FadeIn(prota, shift=RIGHT))

        # Casco vikingo como prop
        helmet = casco_vikingo(pos=RIGHT * 2 + UP * 0.5, escala=1.0)
        self.play(FadeIn(helmet, shift=LEFT))

        # Texto informativo secundario (usamos etiqueta en lugar de callout)
        note = etiqueta(
            "Hierro, protección nasal",
            pos=RIGHT * 3.4 + UP * 1,
            color=ORANGE,
        )
        self.play(FadeIn(note, shift=DOWN))

        self.wait(0.5)

        # Animación del casco girando
        self.play(helmet.animate.rotate(2 * PI), run_time=5)

        self.wait(1)