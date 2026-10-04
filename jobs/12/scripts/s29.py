from manim import *
from zenn_rig import *

class S29(Scene):
    def construct(self):
        # Fondo azul claro
        self.add(fondo(CREMA))

        # Banda de título
        titulo = banda_titulo("Vértigo", color=ORANGE)
        self.play(FadeIn(titulo, shift=UP))
        self.wait(0.8)

        # Sol brillante en esquina superior derecha
        sol_obj = sol(color=YELLOW, radius=0.7, pos=UP * 2.5 + RIGHT * 3)
        self.play(FadeIn(sol_obj, scale=0.5))
        self.wait(0.5)

        # Personaje sintiendo calor (stick_idle) con expresión de sorpresa
        stick = stick_idle(pos=LEFT * 2 + DOWN * 1, height=2.2, color=WHITE)
        self.play(FadeIn(stick, shift=RIGHT))
        self.wait(0.3)
        self.add(expresion(stick, tipo="sorpresa"))
        self.wait(0.4)

        # Llamada visual (callout) y flecha señalando al personaje
        txt = callout("Vértigo", color=ORANGE, font_size=96)
        flecha = arrow(txt.get_center(), stick.get_center(), color=INK, width=8)
        self.play(FadeIn(txt, shift=DOWN), FadeIn(flecha))
        self.wait(0.6)

        # Resaltar al personaje
        rojo = red_accent(stick, scale=1.25)
        self.play(FadeIn(rojo))
        self.wait(1.5)

        # Salida
        self.play(FadeOut(txt), FadeOut(flecha), FadeOut(rojo))
        self.wait(0.5)