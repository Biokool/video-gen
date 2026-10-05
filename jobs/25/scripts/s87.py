from manim import *
from zenn_rig import *

class S87(Scene):
    def construct(self):
        # Fondo espacial: universo/realidad que el cerebro construye
        self.add(fondo(INK))
        self.add(estrellas(n=35, seed=7, color=WHITE))

        # Protagonista "El Porqué" con playera amarilla, señalando y pensando
        prota = protagonista(
            pos=LEFT * 3.5,
            playera="amarilla",
            altura=3.0,
            expresion="pensando",
            pose="senalando"
        )

        # Ojo: la percepción directa limitada
        ojo = ojo_grande(pos=LEFT * 0.8, escala=1.2, iris=TEAL)

        # Universo complejo que la ciencia revela
        universo = planeta(pos=RIGHT * 3.2, radio=1.0, color=TEAL)

        # Etiqueta superior — idea clave
        etiqueta_realidad = etiqueta(
            "la ciencia amplía tu percepción",
            (0, 3.0)
        )

        # Entrada del protagonista y del ojo
        self.play(FadeIn(prota), run_time=1.0)
        self.play(FadeIn(ojo), run_time=0.8)
        self.wait(0.5)

        # El cerebro (fuera de pantalla) está creando el universo
        self.play(Create(universo), run_time=2.0)

        # Momento de entendimiento: expresión cambia
        cambiar_cara(prota, "alegria_pura")

        # La idea aparece con suavidad
        self.play(FadeIn(etiqueta_realidad), run_time=0.6)
        self.wait(2.0)
        self.wait(1.0)