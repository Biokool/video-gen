from manim import *
from zenn_rig import *

class S34(Scene):
    def construct(self):
        self.add(fondo(CREMA))

        banda = banda_titulo("EL MITO DEL CASCO", color=AZUL_MARINO)
        self.play(FadeIn(banda), run_time=0.5)

        linea = camino(pos=DOWN*2.4, width=14)
        self.play(Create(linea), run_time=0.6)

        prota = protagonista(
            pos=LEFT*4.5 + DOWN*1.2,
            playera="azul",
            altura=2.4,
            expresion="pensando",
            pose="caminando"
        )
        self.play(FadeIn(prota), run_time=0.4)

        casco = casco_vikingo(pos=LEFT*4.5 + UP*1.0, escala=0.8)
        self.play(FadeIn(casco), run_time=0.3)

        self.play(
            prota.animate.move_to(LEFT*1 + DOWN*1.2),
            run_time=1.5
        )

        camino_der = camino(pos=RIGHT*3 + DOWN*2.4, width=5)
        camino_der.rotate(-0.2)
        self.play(
            FadeIn(camino_der),
            run_time=0.5
        )

        prota2 = version_prota(
            5,
            pos=LEFT*1 + DOWN*1.2,
            altura=2.4
        )
        self.play(
            Transform(prota, prota2),
            run_time=0.4
        )

        self.play(
            prota.animate.move_to(RIGHT*3 + DOWN*1.2),
            run_time=1.5
        )

        callout_obj = etiqueta(
            "La narrativa pesa\nmás que los hechos",
            pos=RIGHT*2.5 + UP*1.2,
            color=RED,
            font_size=36
        )
        self.play(
            FadeIn(callout_obj),
            run_time=0.5
        )

        self.wait(0.6)