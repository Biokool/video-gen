from manim import *
from zenn_rig import *


class S14(Scene):
    def construct(self):
        # --- Escenario: tres "cajas" del cerebro con una X roja encima ---
        b1 = caja("CEREBRO", pos=RIGHT * 2.8 + UP * 1.3, width=1.9)
        b2 = caja("", pos=RIGHT * 2.8, width=1.9)
        b3 = caja("", pos=RIGHT * 2.8 + DOWN * 1.3, width=1.9)

        self.play(Create(b1), Create(b2), Create(b3), run_time=0.8)
        self.wait(0.2)

        x_mark = VGroup(
            Line(b1.get_corner(UL), b3.get_corner(DR), color=RED, stroke_width=12),
            Line(b1.get_corner(UR), b3.get_corner(DL), color=RED, stroke_width=12),
        )
        self.play(Create(x_mark), run_time=0.5)
        self.wait(0.2)

        # --- Protagonista: el conductor "EL PORQUÉ" ---
        prota = protagonista(
            LEFT * 4.2,
            PLAYERA_AZUL,
            expresion='pensando',
            pose='senalando',
        )
        self.play(FadeIn(prota), run_time=0.7)

        # Señalamiento con flecha del rig (stick_point es solo para monigotes)
        flecha = arrow(prota.get_right(), b1.get_left(), color=INK)
        self.play(Create(flecha), run_time=0.4)

        # --- Callout principal ---
        c = callout("NO ES INSTANTÁNEO", color=CORAL, font_size=76)
        c.move_to(UP * 3.1)
        self.play(FadeIn(c), run_time=0.6)

        # Reacción del protagonista
        cambiar_cara(prota, 'confundido')
        self.wait(0.8)

        # --- Cierre ---
        self.play(
            FadeOut(c),
            FadeOut(flecha),
            FadeOut(x_mark),
            FadeOut(b1),
            FadeOut(b2),
            FadeOut(b3),
            FadeOut(prota),
            run_time=0.8,
        )
        self.wait(0.3)