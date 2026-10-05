from manim import *
from zenn_rig import *

class S43(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=42, color=WHITE))

        prota = protagonista(
            pos=LEFT * 4.2 + DOWN * 0.3,
            playera="amarilla",
            altura=3.0,
            expresion='sorpresa',
            pose='senalando'
        )
        ojo = ojo_grande(pos=LEFT * 5.5 + UP * 1.5, escala=0.8, iris=YELLOW)
        self.play(FadeIn(prota), FadeIn(ojo), run_time=1)

        punto = sol(pos=RIGHT * 2.8 + UP * 0.8, radius=0.12, color=YELLOW)
        self.play(FadeIn(punto), run_time=0.8)
        self.wait(0.3)

        cambiar_cara(prota, 'euforico')
        self.play(punto.animate.scale(8), run_time=2.0)
        self.wait(0.3)

        texto = callout("¡Soles!", color=ORANGE)
        texto.move_to(UP * 2.3 + LEFT * 2)
        self.play(FadeIn(texto), run_time=0.5)
        self.wait(0.6)