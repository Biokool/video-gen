from manim import *
from zenn_rig import *

class S37(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.play(FadeIn(estrellas(n=36, seed=11), shift=UP * 0.3))

        prota = protagonista(pos=LEFT * 3.5 + DOWN * 0.5, playera="rosa",
                             expresion='confundido', pose='de_pie')
        ojo = ojo_grande(pos=RIGHT * 3.7 + UP * 0.8, escala=1.15, iris=CORAL)
        self.play(FadeIn(prota), run_time=0.9)
        self.play(FadeIn(ojo, scale=0.6), run_time=0.9)

        self.play(Write(callout("Un ballet de partículas", color=YELLOW,
                                 font_size=72)).set_run_time(0.8), run_time=0.8)
        cambiar_cara(prota, 'sorpresa')
        self.play(ojo.animate.scale(1.25), run_time=0.4)
        self.play(ojo.animate.scale(1 / 1.25), run_time=0.3)
        self.wait(0.2)

        def lissajous(t, i):
            a = 2 + (i % 3)
            b = 3 + (i % 2)
            rx = 1.05 + 0.12 * (i % 4)
            ry = 0.62 + 0.09 * (i % 3)
            return np.array([rx * np.sin(a * t + i * 0.7),
                             1.15 + ry * np.sin(b * t + i * 1.1), 0])

        cols = [YELLOW, CORAL, TEAL, WHITE, ORANGE, MOSTAZA]
        trk = ValueTracker(0)
        dots = []
        for i in range(18):
            d = Dot(radius=0.075, color=cols[i % len(cols)])
            d.add_updater(lambda m, i=i: m.move_to(lissajous(trk.get_value(), i)))
            dots.append(d)
        self.add(*dots)

        self.play(trk.animate.set_value(6.4), run_time=3.2, rate_func=linear)
        self.play(*[d.animate.scale(0.2) for d in dots], run_time=0.5)
        cambiar_cara(prota, 'pensando')
        self.wait(0.6)