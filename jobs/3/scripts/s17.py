from manim import *
from zenn_rig import *

class S17(Scene):
    def construct(self):
        # Fondo oscuro (bajo la tierra)
        self.add(fondo(INK))
        
        # Título corto
        callout_txt = Text("Bajo miles de metros", color=WHITE, font_size=60)
        callout_txt.to_edge(UP)
        self.play(FadeIn(callout_txt, shift=DOWN * 0.5), run_time=1.0)
        self.wait(0.5)

        # Monigote científico
        fig = stick_idle(LEFT * 3, color=WHITE)
        self.play(FadeIn(fig), run_time=0.5)
        expresion(fig, "preocupado")

        # Experimento (caja con etiqueta)
        caja = caja("XENONnT", RIGHT * 3 + UP * 1)
        red_accent(caja)
        self.play(Create(caja), run_time=1.0)

        # Señalar el experimento
        self.play(stick_point(fig, caja), run_time=0.8)
        self.wait(0.5)

        # Destello de luz (indicador de impacto)
        destello = Circle(radius=0.3, color=YELLOW, fill_opacity=1)
        destello.move_to(caja.get_center() + UP * 0.5)
        self.play(
            FadeIn(destello, scale=0.5),
            Transform(destello, destello.animate.scale(1.5)),
            run_time=1.0
        )
        self.wait(0.5)

        # Expresión de sorpresa al ver el destello
        expresion(fig, "sorpresa")
        self.play(
            FadeOut(destello),
            run_time=0.8
        )

        # Salida
        self.play(
            FadeOut(callout_txt),
            FadeOut(fig),
            FadeOut(caja),
            run_time=1.0
        )
        self.wait(0.5)