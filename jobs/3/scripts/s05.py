from manim import *
from zenn_rig import *

class S05(Scene):
    def construct(self):
        # Galaxy outline
        galaxy_radius = 3.5
        galaxy = Circle(radius=galaxy_radius, color=TEAL, stroke_width=2)
        self.play(Create(galaxy), run_time=1)

        # Inner star
        inner_star_pos = 0.8 * RIGHT
        inner_star = Dot(inner_star_pos, color=YELLOW, radius=0.15)
        self.play(FadeIn(inner_star), run_time=0.5)

        # Outer star
        outer_star_pos = 3.0 * RIGHT
        outer_star = Dot(outer_star_pos, color=ORANGE, radius=0.15)
        self.play(FadeIn(outer_star), run_time=0.5)

        self.wait(1) # Narration: "Esto es lo que esperaríamos en una galaxia."

        # Arrow indicating the radial distance
        # This helps to visually distinguish between 'center' and 'edge'.
        radial_arrow = arrow(ORIGIN, outer_star_pos * 0.9, color=INK) # Arrow points from center to near the outer star
        self.play(Create(radial_arrow), run_time=0.7)
        self.wait(0.5)

        # Animate the stars rotating around the center (ORIGIN)
        # Inner star rotates faster (larger angle)
        # Outer star rotates slower (smaller angle)
        rotation_run_time = 4.0
        inner_rotation_angle = 2 * PI * 0.8 # Almost a full circle
        outer_rotation_angle = 2 * PI * 0.4 # Less than half a circle

        self.play(
            Rotate(inner_star, angle=inner_rotation_angle, about_point=ORIGIN, run_time=rotation_run_time, rate_func=linear),
            Rotate(outer_star, angle=outer_rotation_angle, about_point=ORIGIN, run_time=rotation_run_time, rate_func=linear)
        ) # Narration: "Las estrellas cercanas al centro deberían girar rápido, y las del borde, lento."
        self.wait(0.5)

        # Clean up
        self.play(
            FadeOut(galaxy),
            FadeOut(inner_star),
            FadeOut(outer_star),
            FadeOut(radial_arrow),
            run_time=1
        )
        self.wait(0.3)