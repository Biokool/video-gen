from manim import *
from zenn_rig import *

class S02(Scene):
    def construct(self):
        # Fondo suave y monigote
        self.add(fondo(CREMA))
        
        # Monigote inicial en posición de espera, ligeramente a la izquierda
        stickman = stick_idle(pos=LEFT * 2.5, height=2.2, color=INK)
        self.play(FadeIn(stickman))
        self.wait(0.5)

        # 1. Cierra los ojos
        # `expresion` devuelve un Mobject que representa la cara.
        # Lo añadimos a la escena y lo animamos.
        exp_dormido = expresion(stickman, 'dormido')
        callout_ojos = callout("Cierra los ojos.", color=ORANGE).next_to(stickman, RIGHT, buff=1.0)
        
        # Guardamos la expresión actual para poder transformarla después
        current_expression = exp_dormido 
        
        self.play(
            Create(current_expression), # Animar la aparición de la expresión
            FadeIn(callout_ojos, shift=UP)
        )
        self.wait(1.5)

        # 2. Estira un brazo
        # El monigote apunta a un punto imaginario a su derecha y arriba
        arm_target_stretch = stickman.get_center() + RIGHT * 3 + UP * 0.5
        
        # Creamos el nuevo monigote en la pose de apuntar
        new_stickman_pose = stick_point(stickman, arm_target_stretch)
        
        # Creamos la nueva expresión (normal para apuntar) basada en la nueva pose
        new_expression = expresion(new_stickman_pose, 'normal') 
        
        # Creamos el nuevo callout y lo posicionamos
        callout_brazo = callout("Estira un brazo.").next_to(new_stickman_pose, RIGHT, buff=1.0)
        
        self.play(
            FadeOut(callout_ojos, shift=DOWN),
            Transform(stickman, new_stickman_pose), # Transformar el monigote a la nueva pose
            Transform(current_expression, new_expression), # Transformar la expresión
            FadeIn(callout_brazo, shift=UP)
        )
        # Actualizamos las referencias a los objetos actuales
        stickman = new_stickman_pose
        current_expression = new_expression
        self.wait(1.5)

        # 3. Respira profundamente
        # Volvemos al monigote en reposo, con expresión feliz para relajación
        new_stickman_relaxed = stick_idle(pos=LEFT * 2.5, height=2.2, color=INK)
        new_expression_relaxed = expresion(new_stickman_relaxed, 'feliz')
        callout_respira = callout("Respira profundamente.").next_to(new_stickman_relaxed, RIGHT, buff=1.0)

        self.play(
            FadeOut(callout_brazo, shift=DOWN),
            Transform(stickman, new_stickman_relaxed), # Transformar el monigote a la pose relajada
            Transform(current_expression, new_expression_relaxed), # Transformar la expresión a feliz
            FadeIn(callout_respira, shift=UP)
        )
        # Actualizamos las referencias a los objetos actuales
        stickman = new_stickman_relaxed
        current_expression = new_expression_relaxed
        self.wait(2)

        # Final de la escena: desvanecer todos los elementos
        self.play(
            FadeOut(stickman),
            FadeOut(current_expression),
            FadeOut(callout_respira)
        )
        self.wait(0.5)