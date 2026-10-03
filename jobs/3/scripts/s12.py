from manim import *
from zenn_rig import *

class S12(Scene):
    def construct(self):
        # VOZ: "La materia oscura, posiblemente compuesta por partículas llamadas WIMPs
        # (partículas masivas de interacción débil) o axiones, no tiene carga eléctrica
        # por lo que no interactúa con el campo electromagnético."

        # Monigote aparece y un callout introduce "Materia Oscura".
        fig = stick_idle(LEFT * 4)
        self.play(FadeIn(fig))
        self.wait(0.5)

        dm_callout = callout("MATERIA OSCURA", font_size=72).next_to(fig, UP + RIGHT * 0.5)
        self.play(FadeIn(dm_callout))
        self.wait(1.5)
        self.play(FadeOut(dm_callout))

        # Monigote intenta señalar un punto vacío, simbolizando la falta de interacción directa.
        invisible_target = RIGHT * 3
        
        # El error "TypeError: Unexpected argument Circle passed to Scene.play()"
        # indica que una instancia de Circle se pasó directamente a self.play() sin ser una animación.
        # Las funciones de zenn_rig como `stick_point` y `stick_think` están diseñadas para
        # devolver objetos de animación o mobjects que luego se usan con anim