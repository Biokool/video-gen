from manim import *
from zenn_rig import *

class S03(Scene):
    def construct(self):
        # VOZ: Ese “algo” es la materia oscura.
        # VISUAL: Muestra un callout con "MATERIA OSCURA"
        dark_matter_callout = callout("MATERIA OSCURA")
        self.play(FadeIn(dark_matter_callout))
        self.wait(1.5)
        self.play(FadeOut(dark_matter_callout))
        self.wait(0.5) # Duración total: 2.5s

        # VOZ: No brilla, no absorbe luz y no interactúa con tus ojos.
        # VISUAL: Crea una representación simple de una galaxia/universo.
        num_dots = 15
        universe_elements = VGroup()
        for i in range(num_dots):
            # Crea una espiral de puntos para simular una galaxia
            angle = i * (TAU / num_dots) * 3  # 3 rotaciones completas
            radius_factor = i / num_dots      # El radio aumenta linealmente
            x = radius_factor * np.cos(angle) * 2
            y = radius_factor * np.sin(angle) * 2
            universe_elements.add(Dot(point=ORIGIN + x*RIGHT + y*UP, radius=0.08, color=WHITE))
        universe_elements.shift(UP * 0.5) # Centra el grupo ligeramente hacia arriba

        self.play(Create(universe_elements))
        self.wait(0.5) # Duración total: 3.0s

        # VOZ: Pero sin ella, el universo tal como lo conoces se habría desmoronado hace miles de millones de años.
        # VISUAL: Muestra un acento rojo como advertencia, luego el universo se "desmorona" (se expande).
        # Crea un acento rojo alrededor de los elementos del universo estable para significar peligro.
        # Asumimos que red_accent devuelve un Mobject que puede aparecer/desaparecer.
        red_accent_obj = red_accent(universe_elements)
        self.play(FadeIn(red_accent_obj))
        self.wait(0.5)
        self.play(FadeOut(red_accent_obj))
        self.wait(0.2) # Pequeña pausa antes de la expansión
        # Duración total: 1.2s para el acento + 0.2s = 1.7s. Total acumulado: 4.7s

        # Anima los elementos del universo a expandirse hacia afuera para representar "desmoronarse"
        self.play(
            universe_elements.animate.scale(1.3), # Escala desde su centro
            run_time=2
        )
        self.wait(0.5) # Duración total: 2.5s. Total acumulado: 7.2s

        # VISUAL: Introduce el efecto de la materia oscura: estabilidad.
        # Crea un círculo tenue y transparente para representar el "halo" de materia oscura,
        # implicando su presencia invisible.
        dark_matter_halo = Circle(radius=2.5, stroke_opacity=0.3, stroke_color=TEAL, fill_opacity=0).shift(UP * 0.5)
        self.play(Create(dark_matter_halo)) # Duración: 1.0s. Total acumulado: 8.2s

        # Devuelve los elementos del universo a su tamaño original y estable.
        self.play(
            universe_elements.animate.scale(1/1.3), # Escala de vuelta al tamaño original
            run_time=2
        )
        self.wait(1.5) # Duración total: 3.5s. Total acumulado: 11.7s

        # Desvanece todo al final de la escena.
        self.play(FadeOut(universe_elements), FadeOut(dark_matter_halo))
        self.wait(0.5) # Duración total: 1.0s. Total acumulado: 12.7s