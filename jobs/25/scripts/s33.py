from manim import *
from zenn_rig import *

class S33(Scene):
    def construct(self):
        # Personaje principal (detalles: playera rosa, pensando/analítico)
        el_porque = protagonista(
            pos=(-3.8, -0.5, 0),
            playera="rosa",
            altura=3.0,
            expresion="pensando",
            pose="senalando"
        )
        self.play(FadeIn(el_porque, shift=UP), run_time=0.6)

        # Ojo grande: símbolo de observación / zoom
        lupa = ojo_grande(pos=(-1.2, 1.6, 0), escala=0.9, iris=TEAL)
        self.play(Create(lupa), run_time=0.5)

        # Organelos abstractos con formas únicas
        nucleo = planeta(pos=(1.0, 1.2, 0), radio=0.7, color=AZUL_MARINO)
        mitocondria = curva(pos=(3.2, 1.4, 0), ancho=2.2, alto=1.4, color=INK, acento=RED)
        membrana = red_seguridad(pos=(2.2, -1.2, 0), width=2.0, height=0.6)

        # Entrada escalonada de cada organelo
        for prop in [nucleo, mitocondria, membrana]:
            self.play(FadeIn(prop, scale=0.6), run_time=0.4)
            self.play(Create(red_accent(prop, scale=1.25)), run_time=0.3)
            self.play(prop.animate.scale(0.9), run_time=0.2)

        # Cierre tranquilo: en detalle, cada forma tiene su función
        self.wait(0.5)