from manim import *
from zenn_rig import *

class S029(Scene):
    def construct(self):
        # Protagonist (main character)
        prota = protagonista(
            pos=LEFT*3.5 + DOWN*0.5,
            playera=PLAYERA_VERDE,
            altura=2.5,
            expresion='pregunta',
            pose='de_pie'
        )

        # Simple brain illustration
        cerebro = personaje(
            pos=RIGHT*2.5 + UP*0.5,
            cuerpo=TEAL,
            altura=1.5,
            expresion_tipo='normal'
        )

        # Label for "20% energía"
        label_energia = etiqueta(
            "20% energía",
            pos=RIGHT*2.5 + DOWN*0.5,
            color=INK,
            font_size=40
        )

        # Callout for question sign
        signo_pregunta = callout("?", color=ORANGE, font_size=96).move_to(LEFT*3.5 + UP*1.5)

        # Animations
        self.play(FadeIn(prota), FadeIn(cerebro), run_time=1.5)
        self.play(FadeIn(signo_pregunta), run_time=0.8)
        self.play(Write(label_energia), run_time=0.8)

        # Brain pulse
        self.play(cerebro.animate.scale(1.2), run_time=0.5)
        self.play(cerebro.animate.scale(1/1.2), run_time=0.5)
        self.play(cerebro.animate.scale(1.2), run_time=0.5)
        self.play(cerebro.animate.scale(1/1.2), run_time=0.5)

        # Protagonist slight movement
        self.play(prota.animate.shift(UP*0.2), run_time=0.5)
        self.play(prota.animate.shift(DOWN*0.2), run_time=0.5)

        self.wait(2.0)
        self.wait(0.9)  # total ~9 seconds