from manim import *
from zenn_rig import *

class S16(Scene):
    def construct(self):
        # Fondo nocturno
        self.add(fondo(INK))

        # Protagonista principal (versión azul)
        hero = version_prota(2, pos=LEFT * 3)          # playera azul, altura 3.0
        self.play(FadeIn(hero, run_time=0.6))

        # Cambiamos su expresión a “pensando”
        self.play(cambiar_cara(hero, "pensando"))

        # Ojo grande sobre el héroe
        eye = ojo_grande(pos=hero.get_center() + UP * 0.8, escala=1.0)
        self.play(FadeIn(eye, run_time=0.4))

        # Punto distante que representa la hormiga (monigote muy pequeño)
        distant_point = stick_idle(pos=RIGHT * 5, height=0.2, color=WHITE)
        self.play(FadeIn(distant_point, run_time=0.4))

        # El héroe señala el punto
        self.play(stick_point(hero, distant_point))

        # Callout breve
        call = callout("100 m", color=ORANGE, font_size=96)
        self.play(FadeIn(call, run_time=0.5))

        self.wait(1.0)