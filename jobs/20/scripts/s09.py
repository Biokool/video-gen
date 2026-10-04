from manim import *
from zenn_rig import *

class S09(Scene):
    def construct(self):
        prota = protagonista(LEFT*4.3+DOWN*0.5, PLAYERA_AZUL, altura=3.0,
                             expresion='confundido', pose='senalando')

        cerebro = VGroup(
            Ellipse(width=2.9, height=2.2, color=CORAL, fill_opacity=0.18),
            Arc(radius=0.5, start_angle=PI/2, angle=PI, color=CORAL),
            Arc(radius=0.9, start_angle=PI/2, angle=PI, color=CORAL).shift(DOWN*0.3),
            Arc(radius=1.3, start_angle=PI/2, angle=PI, color=CORAL).shift(DOWN*0.6),
        ).move_to(RIGHT*2.6+UP*0.7)

        nodos = VGroup(*[Dot(cerebro.get_center()+p, radius=0.07, color=TEAL)
                         for p in [LEFT*0.85+UP*0.35, LEFT*0.25+DOWN*0.45,
                                   RIGHT*0.55+UP*0.55, RIGHT*0.95+DOWN*0.30,
                                   UP*0.75+RIGHT*0.10]])

        conex = VGroup(*[Line(nodos[i].get_center(), nodos[j].get_center(),
                              color=TEAL, stroke_width=3)
                         for i, j in [(0,1),(1,2),(2,3),(3,4),(4,0),(1,3)]])

        tache = VGroup(
            Line(LEFT*1.05+UP*0.85, RIGHT*1.05+DOWN*0.85, color=RED, stroke_width=11),
            Line(LEFT*1.05+DOWN*0.85, RIGHT*1.05+UP*0.85, color=RED, stroke_width=11),
        ).move_to(cerebro.get_center())

        aviso = callout("300 s", color=ORANGE, font_size=72).move_to(UP*2.9)

        self.play(FadeIn(prota), FadeIn(cerebro), run_time=0.9)
        self.play(Create(conex), FadeIn(nodos), run_time=1.2)
        self.wait(0.4)

        self.play(FadeIn(aviso, scale=1.2), run_time=0.6)
        cambiar_cara(prota, 'sorpresa')
        self.wait(0.3)

        self.play(Create(tache), run_time=0.8)
        self.play(Indicate(tache, color=RED, scale_factor=1.25), run_time=0.6)
        self.wait(1.2)