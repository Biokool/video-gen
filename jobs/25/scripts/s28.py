from manim import *
from zenn_rig import *

class S28(Scene):
    def construct(self):
        # VOZ: "Cuando usamos un microscopio, entramos en un reino invisible."
        # El protagonista conduce la escena
        prota = protagonista(
            pos=LEFT * 3.2,
            playera=PLAYERA_NARANJA,
            expresion='feliz',
            pose='de_pie'
        )
        self.play(FadeIn(prota), run_time=0.5)

        ojo = ojo_grande(RIGHT * 3.2, escala=1.3, iris=TEAL)
        self.play(FadeIn(ojo, scale=0.4), run_time=0.6)

        # Se acerca al "microscopio" (lente = ojo gigante)
        self.play(prota.animate.shift(RIGHT * 2.2), run_time=1.5)
        cambiar_cara(prota, "sorpresa")

        # El lente se amplía: ilusión de zoom hacia lo invisible
        self.play(ojo.animate.scale(1.35), run_time=0.5)

        etiqueta_reino = etiqueta("reino invisible", (0, 2.6))
        self.play(FadeIn(etiqueta_reino), run_time=0.4)
        self.wait(0.5)