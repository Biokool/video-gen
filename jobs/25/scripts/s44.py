from manim import *
from zenn_rig import *

class S44(Scene):
    def construct(self):
        # Fondo espacial
        fondo_oscuro = fondo(INK)
        estrellas_fondo = estrellas(n=60, seed=7, color=WHITE)
        self.add(fondo_oscuro, estrellas_fondo)

        # Protagonista con playera amarilla, expresión de asombro
        prota = protagonista(
            pos=LEFT * 3.2 + DOWN * 0.5,
            playera="amarilla",
            altura=2.6,
            expresion="sorpresa",
            pose="de_pie"
        )
        self.play(FadeIn(prota, shift=UP * 0.3), run_time=1.2)

        # Ojo grande que observa la distancia
        ojo = ojo_grande(pos=LEFT * 5.2 + UP * 1.7, escala=0.5, iris=TEAL)
        self.play(Create(ojo), run_time=0.8)

        # La estrella lejana: Próxima Centauri
        estrella = sol(pos=RIGHT * 4.8 + UP * 0.6, radius=0.45)
        self.play(FadeIn(estrella, scale=0.6), run_time=0.8)

        # Flecha larga que conecta al protagonista con la estrella
        flecha = arrow(
            start=prota.get_right() + RIGHT * 0.4 + UP * 0.8,
            end=estrella.get_left() - RIGHT * 0.4 + UP * 0.3,
            color=WHITE,
            width=8
        )
        self.play(Create(flecha), run_time=1.5)

        # Etiqueta pequeña identificando a la estrella
        nombre = etiqueta("Próxima Centauri", (3.2, 1.9))
        self.play(FadeIn(nombre, shift=UP * 0.2), run_time=0.8)

        self.wait(1.4)