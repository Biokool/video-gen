from manim import *
from zenn_rig import *

class S51(Scene):
    def construct(self):
        # Fondo oscuro y estrellas
        self.add(fondo(INK))
        cielo = estrellas(n=42, seed=7, color=WHITE)
        self.add(cielo)

        # Protagonista: EL PORQUÉ (obligatorio en toda escena)
        prota = protagonista(
            pos=LEFT * 3.2,
            playera="amarilla",  # mantiene el color original
            altura=3.0,
            expresion="pensando",
            pose="de_pie",
        )
        self.add(prota)

        # Ojo grande al lado: la mirada curiosa de la ciencia
        ojo = ojo_grande(pos=RIGHT * 2.6, escala=0.9, iris=TEAL)
        self.add(ojo)

        # Flecha = telescopio simbólico apuntando hacia las estrellas
        telescopio = arrow(
            start=RIGHT * 0.5 + DOWN * 0.6,
            end=RIGHT * 2.0 + UP * 2.2,
            color=WHITE,
            width=8,
        )
        self.add(telescopio)

        self.play(
            FadeIn(prota, scale=0.9),
            FadeIn(ojo),
            Create(telescopio),
        )

        # El protagonista cambia a expresión feliz
        cambiar_cara(prota, "feliz")
        self.play(ojo.animate.scale(1.15))
        self.wait(2.0)