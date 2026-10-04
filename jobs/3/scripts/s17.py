from manim import *
from zenn_rig import *


class S17(Scene):
    def construct(self):
        def play(obj, run_time=1.0):
            if obj is None:
                self.wait(run_time)
            elif isinstance(obj, Animation):
                self.play(obj, run_time=run_time)
            else:
                self.play(FadeIn(obj), run_time=run_time)

        self.add(fondo(INK))
        play(estrellas(n=30), 1.0)

        fig = stick_idle(pos=LEFT * 3.4, color=WHITE, height=2.2)
        play(fig, 0.9)
        play(expresion(fig, "preocupado"), 0.6)

        flash_graph = curva(
            pos=RIGHT * 2.6,
            ancho=4.2,
            alto=2.4,
            color=WHITE,
            acento=RED,
        )
        play(flash_graph, 1.1)

        label = callout("BAJO ROCA", color=YELLOW, font_size=76).to_edge(UP)
        play(label, 0.8)
        self.wait(1.0)

        play(stick_point(fig, flash_graph.get_center()), 1.4)
        accent = red_accent(flash_graph, scale=1.35)
        play(accent, 1.0)

        flash = callout("DESTELLO", color=ORANGE, font_size=88)
        flash.move_to(flash_graph.get_center() + UP * 1.8)
        self.play(ReplacementTransform(label, flash), run_time=1.0)

        play(stick_think(fig, "¿luz?"), 1.8)
        self.wait(1.4)