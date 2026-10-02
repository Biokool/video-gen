from manim import *
from zenn_rig import *

class S07(Scene):
    def construct(self):
        # Callout breve
        call = callout("Horizonte de sucesos", color=ORANGE, font_size=96)
        self.play(FadeIn(call))
        self.wait(2)
        self.play(FadeOut(call))

        # Agujero negro
        black_hole = Circle(radius=1.5, color=BLACK, fill_opacity=1, stroke_width=0)
        self.play(FadeIn(black_hole))
        self.wait(1)

        # Línea punteada que representa el horizonte
        horizon = DashedLine(
            start=LEFT * 6,
            end=RIGHT * 6,
            color=WHITE,
            dash_length=0.2,
        )
        horizon.set_dash_offset(0.1)   # Ajuste del desplazamiento de los guiones
        self.play(Create(horizon))
        self.wait(1)

        # Monigote inicial
        stick = stick_idle(pos=LEFT * 5 + DOWN * 1, height=2.2, color=INK)
        self.play(FadeIn(stick))
        self.wait(1)

        # Caminata hacia el horizonte
        target_point = black_hole.get_center() + UP * 0.2  # justo encima del horizonte
        stick_walk(stick, target_point, run_time=6.0)
        self.wait(0.5)

        # Efecto de corrimiento al rojo y desvanecimiento
        self.play(
            stick.animate.set_color(RED),
            run_time=3,
        )
        self.wait(0.5)
        self.play(
            stick.animate.set_opacity(0.0),
            run_time=2,
        )
        self.wait(2)

        # Limpieza final
        self.play(FadeOut(black_hole), FadeOut(horizon))
        self.wait(2)