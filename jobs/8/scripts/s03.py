from manim import *
from zenn_rig import * # Assuming zenn_rig.py is in the same directory or accessible

class S03(Scene):
    def construct(self):
        # 1. Initial Setup: Stars, Grid, Stick Figure
        # Create a field of stars
        stars = VGroup(*[Dot(point=np.array([x, y, 0]), radius=0.03, color=WHITE)
                          for x in np.linspace(-6, 6, 25)
                          for y in np.linspace(-4, 4, 18)])
        stars.set_z_index(-1) # Ensure stars are behind other elements

        # Create a spatial grid
        grid = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"stroke_opacity": 0}, # Hide default axes
            background_line_style={
                "stroke_color": INK,
                "stroke_opacity": 0.5,
                "stroke_width": 1,
            }
        ).set_z_index(-2) # Grid furthest back

        # Place the stick figure observing
        figure = stick_idle(pos=LEFT * 4 + UP * 1.5, height=2.0)

        # Introduce initial scene elements
        self.play(
            FadeIn(stars),
            FadeIn(grid),
            FadeIn(figure),
            run_time=2
        )
        self.wait(1)

        # 2. Introduce Black Hole
        black_hole_center = RIGHT * 2
        black_hole = Circle(radius=1.0, color=BLACK, fill_opacity=1.0).move_to(black_hole_center)
        # Add a subtle aura for visual effect
        black_hole_aura = Circle(radius=1.1, color=TEAL, fill_opacity=0.3, stroke_width=0).move_to(black_hole_center)

        self.play(
            GrowFromCenter(black_hole),
            FadeIn(black_hole_aura),
            run_time=1.5
        )
        self.wait(1)

        # 3. Define the distortion function for space-time curvature
        # This function pulls points towards the black hole center,
        # simulating the gravitational lensing and space distortion.
        def deform_space(point):
            bh_c = black_hole.get_center()
            vec_to_bh = bh_c - point
            dist = np.linalg.norm(vec_to_bh)

            if dist < 0.1: # Avoid division by zero or extreme near-center effects
                return point

            # Parameters for the distortion effect
            pull_strength = 0.5 # How strong the pull is
            min_dist_sq = 0.5**2 # Acts as a soft floor for distance in the pull calculation

            # Inverse square-like falloff for the pull factor
            pull_factor = pull_strength / (dist**2 + min_dist_sq)

            # Cap the pull_factor to prevent points from collapsing too much
            pull_factor = min(pull_factor, 0.8) # Don't pull more than 80% towards the center

            return point + vec_to_bh * pull_factor

        # 4. Animate the distortion of the stars and grid
        # Create copies of the original mobjects and apply the distortion function
        distorted_stars = stars.copy().apply_function(deform_space)
        distorted_grid = grid.copy().apply_function(deform_space)

        self.play(
            Transform(stars, distorted_stars),
            Transform(grid, distorted_grid),
            # The original error "TypeError: Unexpected argument Circle passed to Scene.play()"
            # indicates that `stick_point(figure, black_hole.get_center())`
            # returned a Circle Mobject, not an Animation object.
            # `self.play()` expects Animation objects or Mobject.animate calls.
            # If `stick_point` is intended to return an Animation, there might be a bug
            # in its implementation within `zenn_rig.py`.
            # For now, we comment it out to resolve the TypeError.
            # If `stick_point` is meant to modify the figure in place, it should be
            # wrapped in an animation like `ApplyMethod` or `figure.animate.become()`.
            # If it's meant to return an Animation, ensure it does so.
            # For example, if it makes the figure's head look at the target:
            # figure.head.animate.look_at(black_hole.get_center()), # Assuming 'head' exists
            # stick_point(figure, black_hole.get_center()), # Commented out due to TypeError
            run_time=5 # Longer run_time for the main visual effect
        )
        self.wait(4) # Hold the distorted view

        # Add a subtle pulsing effect to the black hole aura
        self.play(
            black_hole_aura.animate.scale(1.05).set_opacity(0.4),
            run_time=1
        )
        self.play(
            black_hole_aura.animate.scale(1/1.05).set_opacity(0.3),
            run_time=1
        )
        self.wait(3.5) # Hold the scene further to reach target duration

        # 5. Fade out all elements
        self.play(
            FadeOut(stars),
            FadeOut(grid),
            FadeOut(figure),
            FadeOut(black_hole),
            FadeOut(black_hole_aura),
            run_time=2
        )