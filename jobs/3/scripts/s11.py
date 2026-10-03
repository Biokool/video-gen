from manim import *
from zenn_rig import *

class S11(Scene):
    def construct(self):
        # Representación de un átomo: un círculo con un punto central como electrón
        atom_circle = Circle(radius=0.8, color=TEAL, fill_opacity=0.5).move_to(ORIGIN)
        electron_dot = Dot(radius=0.15, color=YELLOW).move_to(atom_circle.get_center())
        atom_group = VGroup(atom_circle, electron_dot)

        # Representación de un fotón
        photon_in = Dot(radius=0.1, color=RED).move_to(LEFT * 4)
        photon_out = Dot(radius=0.1, color=RED).move_to(atom_circle.get_center()) # El fotón de salida nace del átomo

        # 1. Introducir el átomo (representando la "materia normal")
        self.play(FadeIn(atom_group), run_time=0.5)
        self.wait(0.2)

        # 2. Resaltar el átomo para enfatizar "materia normal"
        accent = red_accent(atom_circle)
        self.play(Create(accent), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(accent), run_time=0.7)

        # 3. Un fotón entrante interactúa con el átomo (el electrón)
        self.play(
            Create(photon_in),
            photon_in.animate.move_to(atom_circle.get_center()),
            run_time=1.2
        )
        self.remove(photon_in) # El fotón se "absorbe"

        # 4. El electrón se "excita" (se mueve ligeramente)
        electron_excited_pos = electron_dot.get_center() + UP * 0.3
        self.play(electron_dot.animate.move_to(electron_excited_pos), run_time=0.3)
        self.wait(0.3)

        # 5. El electrón vuelve a su estado original y emite un nuevo fotón
        self.play(
            electron_dot.animate.move_to(atom_circle.get_center()),
            Create(photon_out),
            photon_out.animate.move_to(RIGHT * 4),
            run_time=1.2
        )
        self.remove(photon_out) # El fotón se aleja

        # Finalizar la escena
        self.wait(0.5)
        self.play(FadeOut(atom_group), run_time=0.5)