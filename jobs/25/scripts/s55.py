from manim import *
from zenn_rig import *

class S55(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT * 4.5 + DOWN * 1.2,
            playera="amarilla",
            altura=3.0,
            expresion="pensando",
            pose="de_pie"
        )

        ojo1 = ojo_grande(pos=ORIGIN + UP * 0.6, escala=1.0, iris=TEAL)
        ojo2 = ojo_grande(pos=ORIGIN + UP * 0.6, escala=1.0, iris=TEAL)

        micro = matraz(pos=LEFT * 2 + UP * 0.6, escala=0.9, liquido=TEAL)
        tele = planeta(pos=RIGHT * 2 + UP * 0.6, radio=0.65, color=TEAL)

        self.play(FadeIn(prota), run_time=1.0)
        self.play(FadeIn(ojo1, ojo2), run_time=0.8)
        self.play(
            Transform(ojo1, micro),
            Transform(ojo2, tele),
            prota.animate.shift(RIGHT * 0.3),
            run_time=2.0
        )
        cambiar_cara(prota, "feliz")
        self.play(
            FadeIn(red_accent(micro)),
            FadeIn(red_accent(tele)),
            run_time=1.0
        )
        self.wait(1.2)