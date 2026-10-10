from manim import *
from zenn_rig import *

class S78(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN*1.3 + LEFT*4.2,
            playera=PLAYERA_ROJA,
            altura=2.4,
            expresion="pensando",
            pose="de_pie"
        )
        
        g1 = stick_idle(pos=RIGHT*1.5 + UP*0.8, height=2.0, color=INK)
        g2 = stick_idle(pos=RIGHT*3.8 + UP*0.8, height=2.0, color=INK)
        
        expresion(g1, "feliz")
        expresion(g2, "feliz")
        
        c = caja(etiqueta="PIANO", pos=RIGHT*2.65 + DOWN*0.6, width=2.8)
        
        co = callout(
            "Simetría manual\na pesar de la\ndominancia cerebral",
            color=ORANGE,
            pos=RIGHT*3.2 + UP*2.2
        )
        
        self.play(
            FadeIn(prota),
            FadeIn(g1),
            FadeIn(g2),
            FadeIn(c),
            run_time=1.0
        )
        
        self.play(
            FadeIn(co, shift=LEFT),
            run_time=0.8
        )
        
        self.play(
            stick_walk(g1, g1.get_center() + LEFT*0.3),
            stick_walk(g2, g2.get_center() + RIGHT*0.3),
            run_time=1.5
        )
        
        self.wait(6.7)