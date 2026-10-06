from manim import *
from zenn_rig import *

class S03(Scene):
    def construct(self):
        # Fondo nocturno
        self.add(fondo(INK))

        # Título superior
        title = banda_titulo("Efectos de la luz azul", color=YELLOW)
        self.play(FadeIn(title, shift=UP))

        # Protagonista sorprendido
        prota = protagonista(
            pos=DOWN * 1.2 + LEFT * 3.5,
            playera=PLAYERA_NARANJA,
            altura=2.6,
            expresion="sorpresa",
            pose="de_pie",
        )
        self.play(FadeIn(prota, shift=RIGHT))

        # Teléfono (caja con ícono)
        phone = caja("📱", pos=LEFT * 2 + UP * 1, width=0.8)
        self.play(FadeIn(phone, shift=DOWN))

        # Burbuja azul que sale del teléfono
        bubble = etiqueta("🔵", pos=LEFT * 2 + UP * 1 + RIGHT * 0.8, color=TEAL)
        self.play(FadeIn(bubble, shift=UP))

        # Reloj que representa el ritmo circadiano
        clock = reloj_pared(
            radius=1.0,
            pos=RIGHT * 2 + DOWN * 0.5,
            hora_3=True,
        )
        self.play(FadeIn(clock, shift=LEFT))

        # Flecha que indica el “freno” del reloj
        arr = arrow(
            start=bubble.get_center(),
            end=clock.get_center(),
            color=INK,
            width=8,
        )
        self.play(Create(arr))

        # Resaltar el reloj como frenado (red_accent devuelve un Mobject,
        # por lo que lo añadimos con una animación de aparición)
        accent = red_accent(clock, scale=1.25)
        self.play(FadeIn(accent))

        self.wait(2)