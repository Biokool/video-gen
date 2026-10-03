from manim import *
from zenn_rig import *

class S09(Scene):
    def construct(self):
        # VOZ: Los datos del satélite Planck, lanzado por la ESA, nos dan el recuento definitivo.
        title = title_card("DATOS DE PLANCK")
        self.play(Create(title))
        self.wait(1.5)
        self.play(FadeOut(title))

        # VOZ: El universo está compuesto por un 5% de materia visible,
        visible_matter = callout("5% MATERIA VISIBLE", color=YELLOW, font_size=72).to_edge(UP)
        self.play(Create(visible_matter))
        self.wait(2.0)

        # VOZ: un 27% de materia oscura
        dark_matter = callout("27% MATERIA OSCURA", color=ORANGE, font_size=72)
        self.play(Create(dark_matter))
        self.wait(2.0)

        # VOZ: y un 68% de energía oscura.
        dark_energy = callout("68% ENERGÍA OSCURA", color=RED, font_size=72).to_edge(DOWN)
        self.play(Create(dark_energy))
        self.wait(3.0)

        self.play(
            FadeOut(visible_matter),
            FadeOut(dark_matter),
            FadeOut(dark_energy)
        )

        # VOZ: Eso significa que todo lo que has tocado, leído o visto en tu vida
        # representa menos de una sexta parte de la masa total del cosmos.
        fig = stick_idle(pos=LEFT*3)
        self.play(Create(fig))
        self.wait(1.0)

        visible_summary = callout("TODO LO VISIBLE:\n5% DEL COSMOS", color=YELLOW, font_size=64).next_to(fig, RIGHT*2)
        self.play(Create(visible_summary))
        self.wait(3.0)

        self.play(FadeOut(visible_summary))
        self.wait(0.5)

        # VOZ: El 95% restante es invisible.
        # El error "TypeError: Unexpected argument Circle passed to Scene.play()"
        # indica que la función `stick_think` está devolviendo directamente un Mobject (probablemente un Circle
        # que forma parte de la burbuja de pensamiento), en lugar de una animación.
        # Para corregirlo, capturamos el Mobject devuelto y luego lo animamos con `Create()`.
        thought_bubble_mobject = stick_think(fig, "95% INVISIBLE") # stick_think returns the thought bubble Mobject
        self.play(Create(thought_bubble_mobject)) # Animate the creation of the thought bubble
        self.wait(4.0)

        # Asegurarse de que la burbuja de pensamiento también se desvanezca.
        self.play(FadeOut(fig), FadeOut(thought_bubble_mobject))
        self.wait(1.0)