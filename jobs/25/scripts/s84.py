from manim import *
from zenn_rig import *

class S84(Scene):
    def construct(self):
        # Fondo oscuro: la realidad oculta no se ve a simple vista
        self.add(fondo(INK))

        # El Porqué con playera rosa, señalando la capa de realidad
        prota = protagonista(
            LEFT * 3.4,
            playera="rosa",
            altura=2.6,
            expresion="sorpresa",
            pose="senalando"
        )
        self.play(FadeIn(prota), run_time=0.7)

        # El ojo representa la realidad que normalmente no percibimos
        ojo = ojo_grande(
            pos=RIGHT * 3.0,
            escala=0.85,
            iris=TEAL
        )

        # Capa de realidad visible que tapa al ojo
        capa = caja("REALIDAD", pos=RIGHT * 3.0, width=2.8)
        self.play(Create(ojo), FadeIn(capa), run_time=0.8)
        self.wait(0.4)

        # La capa se levanta y aparece la realidad oculta
        self.play(
            capa.animate.shift(UP * 2.5).scale(0.5).set_opacity(0),
            run_time=1.2
        )
        cambiar_cara(prota, "feliz")
        self.play(
            Create(red_accent(ojo)),
            prota.animate.shift(RIGHT * 0.3),
            run_time=0.8
        )
        self.wait(0.6)