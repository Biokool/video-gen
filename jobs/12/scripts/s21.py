from manim import *
from zenn_rig import *

class S21(Scene):
    def construct(self):
        # Fondo neutro
        self.add(fondo(WHITE))

        # Título de la sección
        titulo = banda_titulo("El dolor y la nocicepción", color=ORANGE)
        self.play(FadeIn(titulo, shift=UP), run_time=2)

        # Reloj con iconos de comer, beber y dormir
        reloj = clock_montage(radius=1.6, color=INK)
        self.play(FadeIn(reloj), run_time=2)

        # Monigote relajado en el centro
        monigote = stick_idle(pos=ORIGIN, height=2.2, color=WHITE)
        self.play(FadeIn(monigote), run_time=2)

        # Expresión preocupada (dolor)
        cara = expresion(monigote, tipo="preocupado")
        self.play(FadeIn(cara), run_time=1)

        # Primer callout
        txt1 = callout("Dolor ≠ tacto", color=ORANGE, font_size=96)
        self.play(FadeIn(txt1, shift=UP), run_time=1.5)
        flecha1 = arrow(start=txt1.get_center(), end=monigote.get_center(),
                        color=INK, width=8)
        self.play(Create(flecha1), run_time=1)
        self.wait(2)

        # Segundo callout
        txt2 = callout("Nocicepción", color=YELLOW, font_size=96)
        self.play(FadeIn(txt2, shift=UP), run_time=1.5)
        flecha2 = arrow(start=txt2.get_center(), end=monigote.get_center(),
                        color=INK, width=8)
        self.play(Create(flecha2), run_time=1)
        self.wait(2)

        # Monigote camina hacia la derecha mientras piensa
        destino = monigote.get_center() + 3 * RIGHT
        self.play(
            stick_walk(monigote, destino, run_time=3.0, steps=6),
            stick_think(monigote, "¿Cómo se detecta?"),
            run_time=3.0,
        )
        self.wait(2)

        # Cambio a expresión feliz (entendimiento)
        cara_feliz = expresion(monigote, tipo="feliz")
        self.play(FadeIn(cara_feliz), run_time=1)

        # Cierre con título final
        cierre = titulo_seguro("Fin de la sección", color=TEAL)
        self.play(FadeIn(cierre, shift=DOWN), run_time=2)
        self.wait(2)