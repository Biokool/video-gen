from manim import *
from zenn_rig import *

class S03(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=42, seed=7, color=WHITE))

        protagonista_obj = protagonista(pos=LEFT*2, playera=PLAYERA_NARANJA, expresion='sorpresa', pose='de_pie')
        ojo_gigante_obj = ojo_grande(pos=protagonista_obj.get_center() + UP*0.3 + RIGHT*0.2, escala=0.8, iris=TEAL)
        
        # El error original indicaba 'AttributeError: VGroup object has no attribute 'change_expression''
        # Esto se debe a que el método para cambiar la expresión del protagonista es 'cambiar_cara', no 'change_expression'.
        # También, la función 'explosion' no se encuentra en la API del rig proporcionada.
        # Se asumirá que la intención era hacer que el protagonista tuviera una expresión de "mente explotada".

        self.play(FadeIn(protagonista_obj), Create(ojo_gigante_obj))
        
        # Corregido: usar 'cambiar_cara' en lugar de 'change_expression'
        # Corregido: usar la expresión 'mente_explotada' que sí existe en la lista proporcionada.
        self.play(
            cambiar_cara(protagonista_obj, "mente_explotada"),
            run_time=1.5
        )
        self.wait(0.5)

        # El callout debería tener un objetivo. Si no hay una explosión explícita,
        # se puede hacer que el callout aparezca cerca del protagonista.
        callout_obj = callout("¡BOOM!", color=YELLOW, font_size=96)
        callout_obj.next_to(protagonista_obj, UP, buff=1.0) # Ajustado para que aparezca sobre el protagonista
        
        self.play(FadeIn(callout_obj))
        self.wait(1.0)

        self.play(FadeOut(protagonista_obj, ojo_gigante_obj, callout_obj))