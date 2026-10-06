from manim import *
from zenn_rig import *

class S01(Scene):
    def construct(self):
        # Fondo pastel azul
        self.camera.background_color = "#A0D8EF"

        # Título principal (único en la escena)
        titulo = title_card("¡Hola!", color=ORANGE)
        titulo.to_edge(UP)          # lo colocamos en la zona superior
        self.play(FadeIn(titulo, run_time=0.8))

        # Protagonista con playera naranja, expresión feliz
        prota = protagonista(
            pos=ORIGIN,
            playera=PLAYERA_NARANJA,
            altura=3.0,
            expresion="feliz",
            pose="de_pie",
        )
        self.play(FadeIn(prota, run_time=1.0))

        # Sol pastel en la esquina izquierda‑arriba
        solito = sol()
        solito.move_to(LEFT * 3 + UP * 2)
        self.play(FadeIn(solito, run_time=0.8))

        # Pequeña etiqueta opcional (texto secundario)
        subtitulo = etiqueta(
            texto="Bienvenidos",
            pos=DOWN * 2.5,
            color=WHITE,
            font_size=40,
            ancho_max=5.5,
        )
        self.play(FadeIn(subtitulo, run_time=0.6))
        self.wait(2.0)

        # Desvanecimiento final
        self.play(
            FadeOut(titulo, run_time=0.6),
            FadeOut(subtitulo, run_time=0.6),
            FadeOut(solito, run_time=0.6),
            FadeOut(prota, run_time=0.6),
        )
        self.wait(1.0)