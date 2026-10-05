from manim import *
from zenn_rig import *

class S50(Scene):
    def construct(self):
        # Fondo espacial
        self.add(fondo(INK))
        estrellas_montaje = estrellas(n=80, seed=7)
        self.add(estrellas_montaje)

        # Protagonista con playera amarilla, asombrado
        prota = protagonista(
            pos=LEFT * 3.5 + DOWN * 0.3,
            playera="amarilla",
            altura=3.0,
            expresion="sorpresa",
            pose="de_pie"
        )
        self.play(FadeIn(prota, shift=UP * 0.3), run_time=0.6)

        # Ojo gigante que observa desde fuera
        ojo = ojo_grande(pos=RIGHT * 4.2 + UP * 0.8, escala=0.8)
        self.play(Create(ojo), run_time=0.8)

        # Galaxia entendida como remolino de luz
        giro1 = curva(pos=ORIGIN, ancho=3.2, alto=2.2, color=YELLOW, acento=ORANGE)
        giro2 = giro1.copy().rotate(PI / 3)
        giro3 = giro1.copy().rotate(2 * PI / 3)
        nucleo = sol(pos=ORIGIN, radius=0.4)
        galaxia = VGroup(giro1, giro2, giro3, nucleo).scale(1.1)
        galaxia.move_to(RIGHT * 1.2 + UP * 0.2)

        self.play(Create(galaxia), run_time=0.8)
        self.play(
            Rotate(galaxia, angle=2 * PI, run_time=1.6),
            Rotate(estrellas_montaje, angle=PI / 4, run_time=1.6),
        )
        self.wait(0.2)