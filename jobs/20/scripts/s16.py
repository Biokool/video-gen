from manim import *
from zenn_rig import *


class S16(Scene):
    def construct(self):
        self.add(fondo(WHITE))

        # ----- personaje principal -----
        prota = protagonista(pos=LEFT * 3.5 + DOWN * 0.4,
                             playera=BLUE,
                             expresion='pensando',
                             pose='de_pie')

        # ----- gráfica (firma real: curva(pos, ancho, alto)) -----
        onda = curva(pos=RIGHT * 2.5 + UP * 0.7,
                     ancho=4.8,
                     alto=2.2)

        # ----- textos -----
        t1 = callout("MISMO CABLEADO", color=BLUE_D, font_size=52).to_edge(UP, buff=0.5)
        t2 = etiqueta("MEJOR ENERGÍA", (3.1, -1.75))

        # ----- puntos de la "energía" sobre la gráfica -----
        pts = [(-1.5, 0.1), (-0.6, 0.8), (0.3, 0.2), (1.2, 0.9), (1.9, 0.4)]
        dots = VGroup(*[
            Dot(radius=0.09, color=ORANGE).move_to(
                RIGHT * 2.5 + UP * 1.1 + RIGHT * x + UP * y
            )
            for x, y in pts
        ])

        # ----- animación -----
        self.play(FadeIn(prota, shift=RIGHT * 0.4),
                  Create(onda),
                  run_time=1.2)

        # cambiar_cara(prota, tipo) — firma real
        self.play(cambiar_cara(prota, 'sorpresa'),
                  FadeIn(t1, shift=DOWN * 0.3),
                  run_time=0.8)

        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots],
                              lag_ratio=0.22),
                  run_time=1.4)

        self.play(dots.animate.shift(RIGHT * 0.35).set_opacity(0.45),
                  FadeIn(t2),
                  run_time=1.2)

        self.play(Indicate(onda, color=ORANGE, scale_factor=1.06),
                  run_time=0.7)

        self.wait(0.6)