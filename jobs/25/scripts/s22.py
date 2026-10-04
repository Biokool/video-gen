from manim import *
from zenn_rig import *

class S22(Scene):
    def construct(self):
        # Fondo nocturno (fondo negro)
        self.add(fondo(INK))

        # Protagonista con playera roja y expresión pensativa
        prota = protagonista(
            pos=LEFT * 3,
            playera=PLAYERA_ROJA,
            altura=3.0,
            expresion='pensando',
            pose='de_pie'
        )

        # Ojo grande como detalle
        ojo = ojo_grande(
            pos=RIGHT * 2,
            escala=1.5,
            iris=TEAL
        )

        # Signo de interrogación destacado
        pregunta = callout(
            "¿?",
            color=ORANGE,
            font_size=96
        ).move_to(UP * 2)

        # Flecha que señala del ojo al protagonista
        flecha = arrow(
            start=ojo.get_center(),
            end=prota.get_center(),
            color=INK,
            width=8
        )

        # Animaciones
        self.play(FadeIn(prota, scale=0.8))
        self.play(FadeIn(ojo, scale=0.8))
        self.play(FadeIn(pregunta, scale=0.8))
        self.play(Create(flecha))

        # Pequeña pausa para que el espectador lea
        self.wait(2)

        # Desvanecimiento final
        self.play(
            FadeOut(pregunta),
            FadeOut(flecha),
            FadeOut(ojo),
            FadeOut(prota),
            FadeOut(fondo(INK))
        )