from manim import *
from zenn_rig import *

class S86(Scene):
    def construct(self):
        # Protagonista con playera amarilla (tema pregunta), pensando
        prota = protagonista(
            pos=LEFT * 4.5 + DOWN * 1.0,
            playera="amarilla",
            expresion="pensando",
            pose="de_pie"
        )
        self.play(FadeIn(prota, shift=UP), run_time=1)

        # Iceberg representado por una lápida sin texto (piedra blanca)
        iceberg = lapida(texto=" ", pos=RIGHT * 2.8 + DOWN * 1.4, ancho=2.2)
        self.play(FadeIn(iceberg, shift=UP), run_time=1)

        # Galaxia y célula emergiendo del iceberg
        galaxia = sol(radius=0.6, pos=RIGHT * 4.0 + UP * 1.8)
        celula = ojo_grande(pos=RIGHT * 0.8 + UP * 1.6, escala=0.8, iris=TEAL)

        self.play(
            FadeIn(galaxia, shift=UP),
            FadeIn(celula, shift=UP),
            run_time=2
        )

        # Reacción del protagonista
        cambiar_cara(prota, "sorpresa")
        self.wait(0.5)

        # Mensaje corto (uno solo por escena)
        mensaje = callout("La punta del iceberg", color=ORANGE, font_size=72)
        mensaje.to_edge(UP)
        self.play(Write(mensaje), run_time=1)
        self.wait(1.5)