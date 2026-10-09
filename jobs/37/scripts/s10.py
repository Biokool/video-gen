from manim import *
from zenn_rig import *

class S10(Scene):
    def construct(self):
        # Agregar el fondo de papel
        self.add(fondo_papel())

        # Crear el protagonista
        prota = protagonista(
            pos=LEFT * 2.5 + DOWN * 0.8,
            playera="amarilla",
            altura=2.4,
            expresion="pensando",
            pose="de_pie"
        )
        
        # Elementos de misterio
        misterio_vela = vela(pos=RIGHT * 2.5 + DOWN * 0.8, escala=1.2)
        misterio_lupa = lupa(pos=RIGHT * 2.5 + UP * 0.6, escala=1.1)

        # Animación de entrada
        self.play(
            FadeIn(prota),
            FadeIn(misterio_vela),
            FadeIn(misterio_lupa),
            run_time=0.8
        )

        # Crear fondo oscuro translúcido
        sombra = fondo(INK).set_opacity(0.4)
        
        # Cambiar expresión del protagonista
        cambiar_cara(prota, "sarcastico")

        # Crear el cartel de llamada de atención
        texto_duda = callout("¿QUÉ HAY DETRÁS?", color=YELLOW, pos=RIGHT * 2.5 + UP * 2.1)

        # Mostrar sombra y texto
        self.play(
            FadeIn(sombra),
            FadeIn(texto_duda),
            run_time=1.2
        )

        self.wait(2.0)