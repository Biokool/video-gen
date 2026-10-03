from manim import *
from zenn_rig import *

class S16(Scene):
    def construct(self):
        # Fondo oscuro para simular el entorno de detección de partículas
        self.add(fondo(INK))
        
        # Monigote principal buscando/observando
        fig = stick_idle(LEFT * 3, height=2.5, color=WHITE)
        exp = expresion(fig, "preocupado")
        
        # Añadir los elementos iniciales con FadeIn
        self.play(FadeIn(fig), FadeIn(exp))
        
        # Llamada a la acción visual: "Intentamos atraparla"
        callout_text = "50 AÑOS INTENTANDO ATRAPARLA"
        txt = callout(callout_text, color=YELLOW, font_size=72)
        self.play(TransformFromCopy(exp, txt), run_time=3)
        self.wait(1)
        
        # Movimiento: El monigote camina hacia la derecha simulando el esfuerzo de búsqueda
        stick_walk(fig, RIGHT * 2, run_time=4)
        
        # Expresión cambia a "sorpresa" al mencionar las partículas atravesando la Tierra
        self.play(TransformFromCopy(exp, expresion(fig, "sorpresa")))
        
        # Aparece una representación abstracta de la Tierra y partículas (usando círculos/estrellas como props)
        tierra = Circle(radius=1.5, color=BLUE, fill_opacity=0.3).move_to(RIGHT * 4)
        self.play(Create(tierra), run_time=2)
        
        # Efecto de partículas atravesando (simulado con estrellas pequeñas moviéndose)
        particulas = VGroup(*[Dot(color=WHITE, radius=0.1).move_to(LEFT * 5 + UP * (i - 2)) for i in range(5)])
        self.play(particulas.animate.shift(RIGHT * 9), run_time=3)
        
        # El monigote señala hacia la Tierra/Detector
        # Corrección: En lugar de fig.get_eye() que falla, usamos un punto relativo al monigote o su cabeza
        origen = fig[1].get_center() if len(fig) > 1 else fig.get_center()
        arrow_ref = arrow(origen, tierra.get_center())
        self.play(Create(arrow_ref), run_time=2)
        
        # Callout final sobre el choque débil
        callout_final = "CHOQUE DÉBIL"
        txt_final = callout(callout_final, color=RED, font_size=80)
        self.play(TransformFromCopy(txt, txt_final))
        
        self.wait(2)