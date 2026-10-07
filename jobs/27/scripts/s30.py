from manim import *
from zenn_rig import *


class S30(Scene):
    def construct(self):
        self.add(fondo(INK))
        cielo = estrellas(n=48, seed=7)
        self.play(FadeIn(cielo), run_time=0.6)

        prota = protagonista(pos=LEFT*4.3 + DOWN*1.35, playera="amarilla",
                             altura=2.5, expresion="triste", pose="de_pie")
        self.play(FadeIn(prota, shift=UP*0.3), run_time=0.6)

        manzana = planeta(pos=LEFT*2.0 + UP*1.5, radio=0.42, color=RED)
        astro = sol(pos=RIGHT*4.0 + UP*1.6, radius=0.5, color=YELLOW)
        lbl = etiqueta("manzana", (-2.0, 0.72))
        self.play(FadeIn(manzana, scale=0.6), FadeIn(astro, scale=0.6),
                  FadeIn(lbl), run_time=0.8)

        enlace = arrow(LEFT*1.55 + UP*1.5, RIGHT*3.35 + UP*1.6,
                       color=GREY_B, width=6)
        self.play(Create(enlace), run_time=1.6)

        # red_accent puede devolver una Animation o un Mobject (Circle):
        # hay que envolverlo en Create() si es un Mobject.
        acento = red_accent(astro)
        if isinstance(acento, Animation):
            self.play(acento, run_time=0.7)
        elif isinstance(acento, Mobject):
            self.play(Create(acento), run_time=0.7)
        else:
            self.play(Indicate(astro, color=RED, scale_factor=1.25),
                      run_time=0.7)

        nota = callout("unir la manzana\ncon los astros", color=ORANGE,
                       pos=RIGHT*3.6 + DOWN*1.3)
        self.play(FadeIn(nota, shift=UP*0.2), run_time=0.6)
        self.wait(1.2)