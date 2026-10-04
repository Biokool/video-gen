from manim import *
from zenn_rig import *

class S18(Scene):
    def construct(self):
        # --------------------------------------------------------------------
        # Fondo
        # --------------------------------------------------------------------
        self.add(fondo(YELLOW))

        # --------------------------------------------------------------------
        # Título superior (texto seguro)
        # --------------------------------------------------------------------
        title = banda_titulo("Interocepción", color=ORANGE)
        self.play(FadeIn(title, shift=UP))
        self.wait(1)

        # --------------------------------------------------------------------
        # Grupo de 3 monigotes
        # --------------------------------------------------------------------
        sticks = stick_group(
            3,
            center=LEFT * 2,
            spacing=2.5,
            height=2.2,
            color=WHITE,
            seed=3,
        )
        self.play(FadeIn(sticks, shift=RIGHT))
        self.wait(0.5)

        # Referencias a cada figura
        hunger, thirst, beat = sticks

        # --------------------------------------------------------------------
        # Burbujas de pensamiento
        # --------------------------------------------------------------------
        self.play(FadeIn(stick_think(hunger, "hambre")))
        self.wait(0.5)
        self.play(FadeIn(stick_think(thirst, "sed")))
        self.wait(0.5)
        self.play(FadeIn(stick_think(beat, "latido")))
        self.wait(0.5)

        # --------------------------------------------------------------------
        # Movimiento del monigote "hunger"
        # --------------------------------------------------------------------
        target_pos = hunger.get_center() + RIGHT * 3
        self.play(stick_walk(hunger, target_pos, run_time=2.0))
        self.wait(0.5)

        # --------------------------------------------------------------------
        # Aparece el sol como objetivo del señalamiento
        # --------------------------------------------------------------------
        sun = sol(color=YELLOW, radius=0.7, pos=target_pos + RIGHT * 1.5)
        sun.scale(0.5)                     # escalar antes de aparecer
        self.play(FadeIn(sun))
        self.wait(0.5)

        # --------------------------------------------------------------------
        # "hunger" señala el sol
        # --------------------------------------------------------------------
        self.play(stick_point(hunger, sun))
        self.wait(0.5)

        # --------------------------------------------------------------------
        # Todos los monigotes corren a una nueva posición
        #