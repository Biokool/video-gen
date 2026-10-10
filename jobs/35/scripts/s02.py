from manim import *
from zenn_rig import *

class S02(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=42, seed=7, color=WHITE))

        titulo = banda_titulo("¿Por qué eres zurdo o diestro?", color=ORANGE)
        self.play(Create(titulo))

        prota = protagonista(
            pos=DOWN * 1.2 + LEFT * 3.5,
            altura=2.6,
            playera=PLAYERA_NARANJA,
            expresion="pensando",
            pose="de_pie"
        )
        self.play(FadeIn(prota))

        callout_text = "¿Casi nadie lo sabe!"
        # Se cambió callout a etiqueta para evitar el solapamiento con banda_titulo
        # callout_obj = callout(callout_text, color=ORANGE, pos=RIGHT * 3.4 + UP * 1)
        callout_obj = etiqueta(callout_text, pos=RIGHT * 3.4 + UP * 1, color=ORANGE, font_size=40)
        self.play(FadeIn(callout_obj))

        self.wait(3)