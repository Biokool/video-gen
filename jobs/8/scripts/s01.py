# -*- coding: utf-8 -*-
"""
Manim scene corrected: removes unexpected Mobject arguments passed to Scene.play()
and replaces external stick‑figure helpers with simple built‑in constructions.
"""

from manim import *
import numpy as np


class S01(Scene):
    def construct(self):
        # --------------------------------------------------------------------
        # Fondo de estrellas
        # --------------------------------------------------------------------
        stars = VGroup(
            *[
                Dot(
                    point=2 * RIGHT * np.cos(theta) + 2 * UP * np.sin(theta),
                    radius=0.02,
                    color=WHITE,
                )
                for theta in np.linspace(0, TAU, 30, endpoint=False)
            ]
        ).arrange_in_grid(rows=5, cols=6, buff=0.8).shift(2 * UP + 3 * RIGHT)

        self.play(FadeIn(stars, run_time=2))
        self.wait(0.5)

        # --------------------------------------------------------------------
        # Monigote simple (stick figure)
        # --------------------------------------------------------------------
        head = Circle(radius=0.2, color=WHITE).shift(UP * 0.6)
        body = Line(UP * 0.4, DOWN * 0.6, color=WHITE)
        left_arm = Line(ORIGIN, LEFT * 0.5, color=WHITE).next_to(body, LEFT, buff=0)
        right_arm = Line(ORIGIN, RIGHT * 0.5, color=WHITE).next_to(body, RIGHT, buff=0)
        left_leg = (
            Line(ORIGIN, LEFT * 0.3 + DOWN * 0.5, color=WHITE)
            .next_to(body, LEFT, buff=0)
            .shift(DOWN * 0.6)
        )
        right_leg = (
            Line(ORIGIN, RIGHT * 0.3 + DOWN * 0.5, color=WHITE)
            .next_to(body, RIGHT, buff=0)
            .shift(DOWN * 0.6)
        )
        stick = VGroup(head, body, left_arm, right_arm, left_leg, right_leg)
        stick.move_to(3 * LEFT + 2 * UP)

        self.play(FadeIn(stick, run_time=1))
        self.wait(1)

        # --------------------------------------------------------------------
        # Agujero negro (círculo negro)
        # --------------------------------------------------------------------
        black_hole = Circle(radius=1.0, color=BLACK, fill_opacity=1.0)
        black_hole.shift(2 * RIGHT + DOWN)

        # --------------------------------------------------------------------
        # El monigote camina hacia el agujero negro
        # --------------------------------------------------------------------
        target_pos = black_hole.get_center() + LEFT * 1.2
        self.play(stick.animate.move_to(target_pos), run_time=2.5)
        self.wait(0.5)

        # --------------------------------------------------------------------
        # Aparece el agujero negro
        # --------------------------------------------------------------------
        self.play(Create(black_hole, run_time=2))
        self.wait(0.5)

        # --------------------------------------------------------------------
        # El monigote señala el agujero negro
        # --------------------------------------------------------------------
        # Creamos una línea que simula el brazo apuntando al agujero
        pointing_arm = Line(
            start=stick.get_center() + DOWN * 0.2,
            end=black_hole.get_center(),
            color=WHITE,
        )
        self.play(FadeIn(pointing_arm, run_time=1))
        self.wait(1)

        # --------------------------------------------------------------------
        # Desvanecimiento final
        # --------------------------------------------------------------------
        self.play(
            FadeOut(stick, run_time=1),
            FadeOut(black_hole, run_time=1),
            FadeOut(stars, run_time=1),
            FadeOut(pointing_arm, run_time=1),
        )
        self.wait(0.5)