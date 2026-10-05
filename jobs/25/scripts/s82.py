from manim import *
from zenn_rig import *

class S82(Scene):
    def construct(self):
        # Fondo cósmico
        self.add(fondo(INK))
        stars = estrellas(n=42, seed=42)
        self.add(stars)
        luna(pos=RIGHT * 3.4 + UP * 1.8, radio=1.0, color=YELLOW, bg=INK)
        self.wait(0.5)

        # Protagonista con playera rosa y expresión de asombro
        prota = protagonista(
            pos=LEFT * 3.5,
            playera="rosa",
            altura=3.0,
            expresion="sorpresa",
            pose="de_pie"
        )
        self.play(FadeIn(prota, shift=UP * 0.5), run_time=1.0)
        self.wait(0.3)

        # Ojo gigante que revela el cosmos
        eye = ojo_grande(pos=RIGHT * 3.0 + DOWN * 1.2, escala=1.0, iris=TEAL)
        self.play(Create(eye), run_time=1.5)
        self.wait(0.5)

        # Reacción explosiva de asombro
        cambiar_cara(prota, "mente_explotada")
        self.wait(0.5)

        # Callout corto (único en la escena)
        cosmos_label = callout("Mundo cósmico", color=ORANGE, font_size=96)
        cosmos_label.to_edge(UP)
        self.play(FadeIn(cosmos_label, shift=DOWN * 0.3), run_time=1.0)
        self.wait(1.0)

        # Cierre suave
        self.play(FadeOut(cosmos_label), run_time=0.5)
        self.wait(0.5)