from manim import *
from zenn_rig import *

class S09(Scene):
    def construct(self):
        self.add(fondo_papel())

        banda = banda_titulo("¿DE DÓNDE VIENE EL MITO?", color=ORANGE)
        self.play(FadeIn(banda, shift=DOWN * 0.3), run_time=0.8)

        prota = protagonista(
            pos=DOWN * 1.0 + LEFT * 2.8,
            playera="amarilla",
            altura=2.3,
            expresion="confundido",
            pose="de_pie",
        )
        self.play(FadeIn(prota, shift=UP * 0.4), run_time=0.8)
        self.wait(0.5)

        cambiar_cara(prota, "pensando")

        q1 = Text("?", font_size=36, color=ORANGE).move_to(LEFT * 2.2 + UP * 0.8)
        q2 = Text("?", font_size=28, color=INK).move_to(LEFT * 3.3 + UP * 1.0)
        q3 = Text("?", font_size=44, color=RED).move_to(LEFT * 2.7 + UP * 1.4)
        nube_dudas = VGroup(q1, q2, q3)

        self.play(
            FadeIn(q1, shift=UP * 0.2),
            FadeIn(q2, shift=UP * 0.3),
            FadeIn(q3, shift=UP * 0.4),
            run_time=1.0,
        )
        self.wait(1.0)

        casco = casco_vikingo(pos=RIGHT * 2.8 + DOWN * 0.1, escala=1.0)
        lupa_obj = lupa(pos=RIGHT * 2.8 + UP * 1.1, escala=0.8)
        etq = etiqueta("¿Error de interpretación?", (2.8, -1.6), font_size=34)

        self.play(
            FadeIn(casco, shift=LEFT * 0.4),
            FadeIn(lupa_obj, shift=DOWN * 0.3),
            run_time=1.0,
        )
        self.play(Write(etq), run_time=0.8)

        self.play(
            nube_dudas.animate.shift(UP * 0.15),
            run_time=1.2,
        )
        cambiar_cara(prota, "sorpresa")
        self.wait(2.0)