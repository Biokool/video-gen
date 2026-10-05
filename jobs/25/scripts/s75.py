from manim import *
from zenn_rig import *

class S75(Scene):
    def construct(self):
        # Fondo oscuro para contexto espacial
        self.add(fondo(INK))

        # Protagonista con camisa naranja, pensando
        prota = protagonista(
            pos=LEFT * 3 + DOWN * 0.3,
            playera="naranja",
            altura=3.0,
            expresion="pensando",
            pose="de_pie"
        )
        self.play(FadeIn(prota))
        self.wait(0.2)

        # Gran ojo al lado derecho: la "ventana" al espacio
        ojo = ojo_grande(pos=RIGHT * 3.2 + UP * 1.1, escala=1.2, iris=TEAL)
        self.play(Create(ojo))
        self.wait(0.2)

        # Construcción del telescopio con formas básicas (tubo y lentes)
        tubo = Rectangle(
            width=2.8, height=0.45,
            fill_color=TEAL, fill_opacity=1,
            stroke_color=WHITE, stroke_width=2
        )
        lente_objetivo = Circle(
            radius=0.38, fill_color=BLUE,
            fill_opacity=0.8, stroke_color=WHITE
        ).move_to(tubo.get_left())
        lente_ocular = Circle(
            radius=0.24, fill_color=YELLOW,
            fill_opacity=0.9, stroke_color=WHITE
        ).move_to(tubo.get_right())

        telescopio = VGroup(tubo, lente_objetivo, lente_ocular)
        telescopio.move_to(DOWN * 1.8 + RIGHT * 2.5)

        self.play(Create(telescopio))
        self.wait(0.3)

        # Punto del ojo del protagonista
        ojo_prota = prota.get_top() + RIGHT * 0.35 + UP * 0.1

        # Línea imaginaria para calcular la alineación
        linea = Line(ojo_prota, ojo.get_center())
        angulo = linea.get_angle()
        distancia = linea.get_length()

        # Animar: el telescopio se alinea con el ojo y se estira/sitúa en su sitio
        self.play(
            telescopio.animate
            .rotate(angulo)
            .stretch_to_fit_width(distancia)
            .move_to(ojo_prota + linea.get_unit_vector() * distancia / 2),
            run_time=1.5
        )

        # Expresión de entendimiento iluminado
        self.play(prota.animate.scale(1.2), run_time=0.3)
        self.play(prota.animate.scale(1 / 1.2), run_time=0.3)
        cambiar_cara(prota, "alegria_pura")
        self.play(
            Rotate(prota, angle=0.15, rate_func=there_and_back),
            run_time=0.5
        )
        self.wait(0.5)