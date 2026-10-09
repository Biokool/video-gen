from manim import *
from zenn_rig import *

class S42(Scene):
    def construct(self):
        # Fondo oscuro (noche/espacio) y monigote blanco
        self.add(fondo(INK))

        # Protagonista principal, posición en la zona inferior izquierda
        prota = protagonista(
            pos=DOWN * 1.2 + LEFT * 3.5,
            playera="roja",
            altura=2.6,
            expresion="pensando",
            pose="senalando",
        )
        self.add(prota)

        # Reloj de pared con la aguja a las 3 en la zona superior derecha
        reloj = reloj_pared(
            radius=1.0,
            pos=RIGHT * 3.4 + UP * 1.2,
            hora_3=True,
        )
        self.add(reloj)

        # Telón de fondo detrás del reloj (solo decoración)
        telon = Rectangle(
            width=4.5,
            height=2.8,
            color=TEAL,
        ).shift(RIGHT * 3.4 + UP * 1.2)
        self.add(telon)

        # Animaciones del reloj
        self.play(Create(reloj), run_time=1.5)
        self.play(reloj.animate.shift(LEFT * 6.8), run_time=2.5)
        self.play(FadeOut(reloj), run_time=1)
        self.wait(2)

        # Cambiar la expresión del protagonista a feliz (no se envuelve en self.play)
        cambiar_cara(prota, "feliz")

        # Mostrar un callout (animado con FadeIn para que sea una animación válida)
        texto_callout = callout(
            "Ópera del siglo XIX",
            color=ORANGE,
            pos=RIGHT * 3.4 + UP * 1,
            font_size=60,
            ancho_max=7.0,
        )
        self.play(FadeIn(texto_callout))
        self.wait(4)