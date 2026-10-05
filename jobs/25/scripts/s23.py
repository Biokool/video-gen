from manim import *
from zenn_rig import *

class S23(Scene):
    def construct(self):
        prota = protagonista(pos=LEFT*4.5 + DOWN*1.1, playera='roja', altura=2.4,
                             expresion='confundido', pose='senalando')
        celda = caja('célula', pos=RIGHT*0.6 + UP*1.5, width=1.6)
        ojo = ojo_grande(pos=RIGHT*4.6 + DOWN*0.5, escala=1.0)

        ray_in = VGroup(
            Line(RIGHT*1.4 + UP*2.0, LEFT*1.0 + UP*3.6,
                 stroke_width=3, stroke_opacity=0.35, color=YELLOW),
            Line(RIGHT*1.3 + UP*1.6, LEFT*0.3 + UP*3.7,
                 stroke_width=2, stroke_opacity=0.22, color=YELLOW),
        )
        ray_out = VGroup(
            Line(RIGHT*1.4 + UP*2.0, RIGHT*4.1 + UP*0.7,
                 stroke_width=3, stroke_opacity=0.35, color=YELLOW),
            Line(RIGHT*1.4 + UP*1.6, RIGHT*3.9 + UP*0.35,
                 stroke_width=2, stroke_opacity=0.22, color=YELLOW),
        )
        ray_out.set_z_index(1)
        ray_in.set_z_index(1)

        self.play(FadeIn(prota), FadeIn(celda), FadeIn(ojo), run_time=1.0)
        self.play(Create(ray_in), run_time=1.0)
        cambiar_cara(prota, 'sorpresa')
        self.play(celda.animate.scale(1.10), run_time=0.3)
        self.play(celda.animate.scale(1/1.10), Create(ray_out), run_time=1.0)
        self.play(FadeIn(callout("¡Muy tenue!", color=ORANGE)))
        self.wait(1.0)