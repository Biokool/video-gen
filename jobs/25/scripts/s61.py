from manim import *
from zenn_rig import *

class S61(Scene):
    def construct(self):
        # Fondo cálido para ambiente de estudio
        self.add(fondo(CREMA))

        # Protagonista con playera verde, pensando / conocimiento
        prota = protagonista(
            pos=LEFT * 3.4,
            playera="verde",
            altura=3.0,
            expresion="pensando",
            pose="de_pie"
        )
        self.play(FadeIn(prota, shift=UP * 0.3), run_time=0.8)
        self.wait(0.2)

        # Ojo grande: percepción visual
        ojo = ojo_grande(pos=RIGHT * 3.2 + UP * 1.2, escala=1.3, iris=TEAL)
        self.play(Create(ojo), run_time=1.0)
        self.play(ojo.animate.shift(UP * 0.15), run_time=0.5)
        self.wait(0.2)

        # Silueta de cerebro con notas científicas
        lobulo_izq = Circle(radius=0.9, color=INK, fill_opacity=0.25, fill_color=TEAL).shift(LEFT * 0.5)
        lobulo_der = Circle(radius=0.9, color=INK, fill_opacity=0.25, fill_color=TEAL).shift(RIGHT * 0.5)
        tronco = RoundedRectangle(
            corner_radius=0.3, width=1.0, height=0.6,
            color=INK, fill_opacity=0.25, fill_color=TEAL
        ).shift(DOWN * 0.8)
        cisura = Line(ORIGIN, DOWN * 0.45, color=INK, stroke_width=3)

        cerebro = VGroup(lobulo_izq, lobulo_der, tronco, cisura).scale(1.2).move_to(ORIGIN + UP * 0.2)
        self.play(Create(cerebro), run_time=1.2)
        self.wait(0.3)

        # Notas científicas breves
        nota1 = etiqueta("Westheimer", (0.0, 2.2), color=INK, font_size=36)
        nota2 = etiqueta("cortex visual", (0.0, -1.6), color=INK, font_size=30)
        self.play(FadeIn(nota1, shift=DOWN * 0.2), FadeIn(nota2, shift=UP * 0.2), run_time=0.8)
        self.wait(0.2)

        # Cierre: expresión de comprensión / conocimiento
        cambiar_cara(prota, "decidido")
        self.play(prota.animate.shift(UP * 0.1), run_time=0.5)
        self.wait(1.0)

        # Salida limpia
        self.play(
            FadeOut(prota), FadeOut(ojo), FadeOut(cerebro),
            FadeOut(nota1), FadeOut(nota2),
            run_time=0.8
        )
        self.wait(0.2)