from manim import *
from zenn_rig import *

class S12(Scene):
    def construct(self):
        # Fondo rosa pastel
        self.add(fondo(CORAL))

        # Título superior
        titulo = banda_titulo("Propiocepción", color=ORANGE)
        self.play(FadeIn(titulo, shift=UP))

        # Personaje con expresión feliz (cierra los ojos al bailar)
        pers = personaje(
            pos=LEFT * 3,
            cuerpo=TEAL,
            altura=2.6,
            expresion_tipo="feliz",
        )
        self.play(FadeIn(pers, shift=RIGHT))

        # Curva que envuelve al personaje (movimiento fluido)
        cur = curva(
            pos=ORIGIN,
            ancho=5.2,
            alto=2.8,
            color=INK,
            acento=RED,
        )
        self.play(Create(cur, run_time=1.5))

        # Punto de referencia para que el stick lo apunte
        punto_curva = Dot(radius=0.08, color=RED).move_to(cur)
        self.add(punto_curva)

        # Callout breve
        txt = callout("Sensación interna", color=ORANGE, font_size=96)
        self.play(FadeIn(txt, shift=DOWN))

        self.wait(0.8)

        # Personaje se desplaza ligeramente dentro de la curva
        self.play(
            pers.animate.shift(RIGHT * 4),
            run_time=2.0,
        )
        self.wait(0.6)

        # Señalamos la curva
        self.play(stick_point(pers, punto_curva))
        self.wait(0.5)

        # Pensamiento del personaje
        self.play(stick_think(pers, "¡Qué fluido!"))
        self.wait(1.0)

        # Salida
        self.play(
            FadeOut(pers),
            FadeOut(cur),
            FadeOut(txt),
            FadeOut(titulo),
            FadeOut(punto_curva),
        )
        self.wait(0.5)