from manim import *
from zenn_rig import *

class S10(Scene):
    def construct(self):
        # 1. Fondo de la escena
        self.add(fondo(CREMA))

        # 2. Título principal (zona superior segura)
        title = banda_titulo("TU MAPA CORPORAL INVISIBLE: LA PROPIOCEPCIÓN", color=ORANGE)
        self.add(title)

        # 3. Elementos del lado izquierdo: Camino y Personaje
        path = camino(width=4.5, pos=[-3.5, -1.9, 0])
        stick = stick_idle(pos=[-4.5, -0.8, 0], height=2.2, color=INK)

        self.play(Create(path), FadeIn(stick))

        # El personaje camina de forma segura sin mirar al suelo
        self.play(stick_walk(stick, [-2.0, -0.8, 0], run_time=2.0))
        
        # Aparece su expresión de tranquilidad/felicidad
        face = expresion(stick, "feliz")
        self.play(FadeIn(face))
        self.wait(1.0)

        # 4. Elementos del lado derecho (Fase 1: Comida y Ojo)
        cake = pastel(pos=[3.0, -0.8, 0], width=1.5)
        eye = ojo_grande(pos=[3.0, 1.0, 0], escala=0.8)
        lbl_eye = etiqueta("OJO", [3.0, 1.9, 0])
        lbl_food = etiqueta("COMIDA", [3.0, -1.7, 0])

        self.play(
            FadeIn(cake),
            FadeIn(eye),
            Write(lbl_eye),
            Write(lbl_food)
        )
        self.wait(3.0)

        # 5. Transición al concepto de GPS Interno (Fase 2)
        self.play(
            FadeOut(cake),
            FadeOut(eye),
            FadeOut(lbl_eye),
            FadeOut(lbl_food)
        )

        gps_lbl = callout("GPS INTERNO", color=MOSTAZA, font_size=72).move_to([3.0, 0.8, 0])
        map_prop = curva(pos=[3.0, -0.8, 0], ancho=3.5, alto=1.8)

        self.play(
            FadeIn(gps_lbl),
            Create(map_prop)
        )

        # El personaje señala el mapa con sorpresa/descubrimiento
        face_surprise = expresion(stick, "sorpresa")
        self.play(
            Transform(stick, stick_point(stick, gps_lbl.get_center())),
            Transform(face, face_surprise)
        )
        self.wait(3.5)