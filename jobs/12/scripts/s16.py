from manim import *
from zenn_rig import *

class S16(Scene):
    def construct(self):
        # --------------------------------------------------------------------
        # Fondo nocturno
        # --------------------------------------------------------------------
        self.add(fondo(INK))
        self.add(estrellas(n=42, seed=7, color=WHITE))

        # --------------------------------------------------------------------
        # Título superior (texto auto‑escalado)
        # --------------------------------------------------------------------
        titulo = banda_titulo("Percepción Interoceptiva", color=ORANGE)
        self.play(FadeIn(titulo, shift=UP))
        self.wait(0.8)

        # --------------------------------------------------------------------
        # Personaje (monigote) a la izquierda
        # --------------------------------------------------------------------
        figura = stick_idle(pos=LEFT * 3, height=2.2, color=WHITE)
        self.play(FadeIn(figura, shift=RIGHT))
        # expresión de sorpresa
        self.play(FadeIn(expresion(figura, tipo="sorpresa")))
        self.wait(0.5)

        # --------------------------------------------------------------------
        # Luna a la derecha
        # --------------------------------------------------------------------
        luna_obj = luna(pos=RIGHT * 3, radio=1.0, color=YELLOW, bg=INK)
        self.play(FadeIn(luna_obj, shift=LEFT))
        self.wait(0.5)

        # --------------------------------------------------------------------
        # Callout central (pregunta)
        # --------------------------------------------------------------------
        pregunta = callout("¿Escuchar el cuerpo?", color=ORANGE, font_size=96)
        self.play(FadeIn(pregunta, scale=0.8))
        self.wait(0.5)

        # --------------------------------------------------------------------
        # Flecha del monigote al callout
        # --------------------------------------------------------------------
        flecha = arrow(figura.get_center(), pregunta.get_center(),
                       color=WHITE, width=8)
        self.play(FadeIn(flecha))
        self.wait(0.5)

        # --------------------------------------------------------------------
        # El monigote camina hacia el callout
        # --------------------------------------------------------------------
        self.play(
            stick_walk(
                figura,
                pregunta.get_center(),
                run_time=2.0,
                steps=6,
            )
        )
        self.wait(0.3)

        # --------------------------------------------------------------------
        # Señala el callout y piensa en una respuesta
        # --------------------------------------------------------------------
        self.play(FadeIn(stick_point(figura, pregunta.get_center())))
        self.wait(0.3)

        pensamiento = stick_think(figura, "¡Escuchar es sentir!")
        self.play(FadeIn(pensamiento))
        self.wait(1.5)

        # --------------------------------------------------------------------
        # Despedida: desaparece todo
        # --------------------------------------------------------------------
        self.play(FadeOut(VGroup(titulo, figura, luna_obj, pregunta, flecha,
                                 pensamiento)))
        self.wait(0.5)