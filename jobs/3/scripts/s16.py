from manim import *
from zenn_rig import *

class S16(Scene):
    def construct(self):
        self.add(fondo(WHITE))

        fig = stick_idle(LEFT * 4.2, height=2.2, color=INK)
        self.play(FadeIn(fig), run_time=1.2)

        cara = expresion(fig, "preocupado")
        self.play(FadeIn(cara), run_time=1.0)
        self.wait(0.7)

        tierra = planeta(ORIGIN, 1.25, TEAL)
        detector = caja("DETECTOR", RIGHT * 4.2)
        self.play(FadeIn(tierra), FadeIn(detector), run_time=1.5)

        flecha = arrow(tierra.get_right(), detector.get_left())
        self.play(Create(flecha), run_time=1.0)
        self.wait(0.7)

        self.play(stick_point(fig, detector), run_time=1.5)
        self.wait(0.9)

        aviso = callout("50 AÑOS", ORANGE, font_size=80).to_edge(UP)
        self.play(FadeIn(aviso), run_time=1.2)

        aviso2 = callout("CHOCAN DÉBILMENTE", RED, font_size=64).to_edge(UP)
        self.play(FadeOut(aviso), FadeIn(aviso2), run_time=1.2)
        self.wait(1.4)

        self.play(FadeOut(VGroup(fig, cara, tierra, detector, flecha, aviso2)), run_time=1.2)
        self.wait(0.5)