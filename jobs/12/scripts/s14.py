from manim import *
from zenn_rig import *

class S14(Scene):
    def construct(self):
        # Fondo nocturno
        self.add(fondo(INK))

        # Título superior (banda segura)
        titulo = banda_titulo("Sentido interno", ORANGE)
        self.play(FadeIn(titulo))
        self.wait(1)

        # Monigote pensativo (izquierda)
        stick = stick_idle(pos=LEFT * 3, height=2.2, color=WHITE)
        self.play(FadeIn(stick))
        self.play(FadeIn(expresion(stick, "preocupado")))
        self.wait(0.5)

        # Grupo de músculos (centro‑izquierda)
        muscle = stick_group(
            5,
            center=LEFT * 2 + UP * 1,
            spacing=0.8,
            height=1.5,
            color=CORAL,
        )
        self.play(FadeIn(muscle))
        # puntero del monigote al grupo
        point_muscle = stick_point(stick, muscle.get_center())
        self.play(FadeIn(point_muscle))
        self.wait(0.5)

        # Articulación (curva) – centro‑derecha
        joint = curva(
            pos=RIGHT * 2 + UP * 0.5,
            ancho=3,
            alto=1.5,
            color=TEAL,
            acento=RED,
        )
        self.play(FadeIn(joint))
        # puntero del monigote a la articulación
        point_joint = stick_point(stick, joint.get_center())
        self.play(FadeIn(point_joint))
        self.wait(0.5)

        # Flecha al “cerebro” imaginario (arriba centro)
        brain_pos = UP * 2
        self.play(Create(arrow(joint.get_center(), brain_pos, color=WHITE, width=8)))
        self.play(red_accent(joint))
        self.wait(0.5)

        # Callout breve
        mensaje = callout("¡Escucha tu cuerpo!", ORANGE, font_size=96)
        self.play(FadeIn(mensaje))
        self.wait(1)

        # Etiquetas
        etiqueta_musculo = etiqueta(
            "Músculo",
            (muscle.get_center()[0], muscle.get_center()[1] - 1.2),
        )
        etiqueta_articulacion = etiqueta(
            "Articulación",
            (joint.get_center()[0], joint.get_center()[1] - 1.2),
        )
        self.play(FadeIn(etiqueta_musculo))
        self.play(FadeIn(etiqueta_articulacion))
        self.wait(1)

        # Salida
        self.play(
            FadeOut(
                VGroup(
                    stick,
                    muscle,
                    joint,
                    point_muscle,
                    point_joint,
                    mensaje,
                )
            )
        )
        self.play(FadeOut(titulo))
        self.wait(0.5)