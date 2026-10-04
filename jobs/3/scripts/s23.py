from manim import *
from zenn_rig import *


class S23(Scene):
    def _play_any(self, obj, **kwargs):
        if obj is None:
            return
        if isinstance(obj, Animation):
            self.play(obj, **kwargs)
        else:
            self.play(FadeIn(obj, **kwargs))

    def construct(self):
        self.add(fondo(INK))

        stars = estrellas(n=42, seed=7, color=WHITE)
        self.play(FadeIn(stars, run_time=1.0))

        planet = planeta(pos=RIGHT * 2.8, radio=0.95, color=TEAL)
        self.play(Create(planet, run_time=1.2))

        fig = stick_idle(pos=LEFT * 4.2, color=WHITE)
        self.play(FadeIn(fig, run_time=0.6))

        self._play_any(
            stick_walk(fig, LEFT * 2.4, run_time=2.0, steps=6),
            run_time=2.0,
        )
        self.add(expresion(fig, "sorpresa"))

        self._play_any(
            stick_point(fig, planet.get_center()),
            run_time=1.0,
        )

        self._play_any(red_accent(planet), run_time=0.6)

        call = callout("INVISIBLE", color=ORANGE)
        self._play_any(call, run_time=0.6)
        self.wait(1.0)

        self._play_any(
            Transform(call, callout("DOMINA", color=YELLOW)),
            run_time=0.7,
        )
        self.wait(1.2)

        self._play_any(
            Transform(call, callout("COSMOS", color=RED)),
            run_time=0.7,
        )
        self.wait(1.5)