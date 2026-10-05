from manim import *
from zenn_rig import *

class S81(Scene):
    def construct(self):
        self.add(fondo(CREMA))

        prota = protagonista(
            pos=LEFT * 3 + DOWN * 0.6,
            playera="rosa",
            altura=3.0,
            expresion="feliz",
            pose="de_pie",
        )
        ojo = ojo_grande(pos=RIGHT * 3.4 + UP * 0.8, escala=0.9, iris=TEAL)
        vela_obj = vela(pos=RIGHT * 3.4 + DOWN * 1.6, escala=0.8)
        detalle = caja(etiqueta="texturas", pos=RIGHT * 1.6 + DOWN * 1.8, width=1.4)
        etiqueta_txt = etiqueta("detalles y texturas", (0, 2.9), color=INK, font_size=40)

        self.add(etiqueta_txt)

        self.play(
            FadeIn(prota, shift=UP * 0.3),
            Create(ojo),
            FadeIn(vela_obj, shift=UP * 0.2),
            FadeIn(detalle, shift=UP * 0.2),
            run_time=1.5,
        )

        self.play(prota.animate.shift(RIGHT * 0.2), run_time=0.8)
        cambiar_cara(prota, "sorpresa")
        self.play(prota.animate.shift(LEFT * 0.2), run_time=0.8)
        self.wait(0.8)