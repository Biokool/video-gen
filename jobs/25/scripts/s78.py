from manim import *
from zenn_rig import *

class S78(Scene):
    def construct(self):
        # Protagonista reflexivo con playera naranja
        prota = protagonista(
            pos=LEFT * 4.0,
            playera=PLAYERA_NARANJA,
            altura=3.0,
            expresion='pensando',
            pose='de_pie'
        )

        # Ojo, microscopio y telescopio alineados
        ojo = ojo_grande(pos=LEFT * 1.4, escala=1.0, iris=TEAL)
        micro = caja('microscopio', pos=RIGHT * 1.6, width=2.2)
        tele = caja('telescopio', pos=RIGHT * 4.6, width=2.2)

        # Entrada suave de los elementos
        self.play(FadeIn(prota))
        self.play(Create(ojo), run_time=0.8)
        self.play(Create(micro), run_time=0.8)
        self.play(Create(tele), run_time=0.8)
        self.wait(0.6)

        # El protagonista señala la secuencia de herramientas
        self.play(prota.animate.shift(UP * 0.1), run_time=0.4)
        cambiar_cara(prota, 'decidido')

        # Refuerza visualmente cada herramienta con un acento rojo
        acento_ojo = red_accent(ojo)
        acento_micro = red_accent(micro)
        acento_tele = red_accent(tele)
        self.play(Create(acento_ojo), run_time=0.6)
        self.play(Create(acento_micro), run_time=0.6)
        self.play(Create(acento_tele), run_time=0.6)
        self.wait(0.8)

        # Cierre breve con todo en pantalla
        self.play(
            FadeOut(prota),
            FadeOut(ojo),
            FadeOut(micro),
            FadeOut(tele),
            FadeOut(acento_ojo),
            FadeOut(acento_micro),
            FadeOut(acento_tele),
            run_time=0.8
        )
        self.wait(0.2)