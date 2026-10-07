from manim import *
from zenn_rig import *


class S25(Scene):
    def construct(self):
        self.add(fondo_papel())

        prota = protagonista(pos=DOWN * 1.4 + LEFT * 4.0, playera="amarilla",
                             altura=2.6, expresion="alegria_pura", pose="senalando")
        mundo = planeta(pos=UP * 1.9 + RIGHT * 4.4, radio=0.95, color=TEAL)
        orbita = Circle(radius=1.5, color=TEAL, stroke_width=2,
                        stroke_opacity=0.55).move_to(mundo.get_center())
        orbita2 = Circle(radius=2.4, color=TEAL, stroke_width=2,
                         stroke_opacity=0.3).move_to(mundo.get_center())

        self.play(FadeIn(prota, shift=RIGHT * 0.5),
                  FadeIn(mundo, scale=0.7),
                  Create(orbita), Create(orbita2),
                  run_time=1.4)
        self.wait(0.4)

        flecha = arrow(start=DOWN * 0.9 + LEFT * 1.4,
                       end=UP * 1.2 + RIGHT * 2.5, color=INK)
        self.play(Create(flecha), run_time=0.8)

        ley = callout("F = G(m1·m2) / r2", color=YELLOW,
                      font_size=56, pos=RIGHT * 3.8 + DOWN * 1.4)
        self.play(FadeIn(ley, shift=UP * 0.4), run_time=1.1)
        self.wait(0.5)

        acento = red_accent(ley)
        self.play(Create(acento), run_time=1.2)
        self.play(Rotate(orbita, angle=TAU / 3, about_point=mundo.get_center(),
                         rate_func=linear), run_time=1.6)
        self.wait(1.2)