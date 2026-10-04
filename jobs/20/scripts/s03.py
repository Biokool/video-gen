from manim import *
from zenn_rig import *

class S03(Scene):
    def construct(self):
        # Protagonista escéptico (playera naranja)
        prota = protagonista(pos=LEFT*3, playera=PLAYERA_NARANJA, expresion='sarcastico')
        self.play(FadeIn(prota))

        # Reloj de pared para representar el tiempo
        reloj = reloj_pared(radius=0.8, pos=ORIGIN + UP*0.5)
        
        # Texto "5 min" para especificar la duración
        min_text = Text("5 min", font_size=48, color=INK).next_to(reloj, DOWN)

        self.play(FadeIn(reloj, shift=UP), FadeIn(min_text, shift=UP))

        # Gran signo de interrogación
        # El error de ValueError con Wiggle en objetos Text complejos a veces
        # ocurre porque Text es un VGroup de SVGMobjects, y la animación
        # interna de Wiggle puede tener problemas con la inconsistencia
        # de puntos entre submobjects.
        # Una solución es convertir el objeto Text en un único VMobject
        # usando .become() antes de animarlo, lo que "aplana" su estructura.
        
        # 1. Creamos el objeto Text.
        temp_question_mark_text = Text("?", font_size=120, color=ORANGE)
        
        # 2. Posicionamos el objeto Text.
        temp_question_mark_text.next_to(reloj, RIGHT*2)

        # 3. Creamos un VMobject vacío.
        question_mark = VMobject()
        
        # 4. Hacemos que el VMobject vacío adopte la forma del Text.
        #    Esto lo convierte en un único VMobject en lugar de un VGroup.
        question_mark.become(temp_question_mark_text)
        
        # 5. Animamos la creación del signo de interrogación.
        self.play(Create(question_mark))
        
        # 6. Una vez creado, aplicamos la animación Wiggle.
        #    Es importante separar Create de Wiggle para evitar conflictos
        #    en la manipulación de puntos del objeto.
        self.play(Wiggle(question_mark, scale_value=1.1, rotation_angle=0.05 * TAU, run_time=1.0))
        
        self.wait(6) # Duración para la narración