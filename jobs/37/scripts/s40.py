from manim import *
from zenn_rig import *

class S40(Scene):
    def construct(self):
        self.add(fondo_papel())

        banda = banda_titulo("¿CÓMO IMAGINAS A UN VIKINGO?", color=ORANGE)

        prota = protagonista(
            pos=DOWN * 1.2 + LEFT * 3.2,
            playera="amarilla",
            altura=2.5,
            expresion="pensando",
            pose="de_pie"
        )

        q_mark = etiqueta("?", pos=RIGHT * 3.4 + UP * 1.0, color=INK, font_size=56)

        self.play(
            FadeIn(banda),
            FadeIn(prota),
            FadeIn(q_mark),
            run_time=1.0
        )
        self.wait(2.0)

        helmet = casco_vikingo(pos=RIGHT * 3.0 + DOWN * 0.2, escala=1.5)
        label_myth = etiqueta("Imaginario cultural", pos=RIGHT * 3.0 + UP * 1.5, color=INK, font_size=38)

        self.play(
            Create(helmet),
            FadeIn(label_myth),
            run_time=1.2
        )
        self.wait(1.5)

        cambiar_cara(prota, "confundido")
        self.play(
            q_mark.animate.scale(1.2).set_color(RED),
            run_time=0.8
        )
        self.wait(2.5)