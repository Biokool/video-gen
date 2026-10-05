from manim import *
from zenn_rig import *

class S57(Scene):
    def construct(self):
        prota = protagonista(
            pos=LEFT * 3.2 + DOWN * 0.5,
            playera=PLAYERA_NARANJA,
            altura=3.0,
            expresion='pensando',
            pose='senalando'
        )
        ojo = ojo_grande(pos=RIGHT * 2.8 + UP * 2.2, escala=0.7)

        stick_peq = stick_idle(pos=RIGHT * 2.0 + DOWN * 1.2, height=1.0, color=INK)
        stick_med = stick_idle(pos=RIGHT * 3.2 + DOWN * 1.0, height=1.6, color=INK)
        stick_gde = stick_idle(pos=RIGHT * 4.2 + DOWN * 0.8, height=2.2, color=INK)
        expresion(stick_med, 'feliz')

        self.play(FadeIn(prota), FadeIn(ojo), run_time=0.8)
        self.play(
            FadeIn(stick_peq),
            FadeIn(stick_med),
            FadeIn(stick_gde),
            run_time=1.0
        )
        # cambiar_cara() modifica la expresión en el acto,
        # no es una animación para Scene.play()
        cambiar_cara(prota, 'feliz')
        self.wait(0.4)
        self.wait(0.8)