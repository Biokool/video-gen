from zenn_rig import *
from manim import *
import numpy as np
import random

class S16(Scene):
    def construct(self):
        # Fondo oscuro para ambiente espacial/nocturno
        self.camera.background_color = BLACK
        
        # Estrellas para reforzar el ambiente
        stars = VGroup(*[
            Dot(radius=0.02, color=WHITE, z_index=0).move_to(
                [random.uniform(-8, 8), random.uniform(-4, 4), 0]
            ) for _ in range(15)
        ])
        self.add(stars)

        # Usar el rig para el monigote
        fig = figure()
        fig.move_to(LEFT * 3)
        
        self.play(FadeIn(fig), run_time=1.0)

        # Expresión preocupada/seria
        # Ajustar ojos del rig
        if hasattr(fig, 'eye_l') and hasattr(fig, 'eye_r'):
            eye_l = fig.eye_l
            eye_r = fig.eye_r
        else:
            # Fallback si el rig no tiene ojos accesibles directamente
            eye_l = Dot(radius=0.05, color=WHITE).next_to(fig.head, DOWN, buff=0.1).shift(LEFT*0.1)
            eye_r = Dot(radius=0.05, color=WHITE).next_to(fig.head, DOWN, buff=0.1).shift(RIGHT*0.1)
            fig.add(eye_l, eye_r)
        
        # Añadir boca seria
        mouth_serious = Line(LEFT*0.1, RIGHT*0.1, color=WHITE, stroke_width=2).next_to(eye_l, DOWN, buff=0.15)
        
        self.play(
            eye_l.animate.shift(DOWN*0.05),
            eye_r.animate.shift(DOWN*0.05),
            Create(mouth_serious),
            run_time=0.5
        )

        # Prop: curva gráfica (representa detección/interacción)
        curve_func = lambda x: 0.5 * np.sin(x)
        gr = ParametricFunction(
            lambda t: np.array([t, curve_func(t), 0]),
            t_range=[-1, 1, 0.1],
            color=BLUE
        ).scale(1.5).move_to(RIGHT * 3)
        
        # Punto rojo en la curva
        red_dot = Dot(color=RED).move_to(gr.point_from_proportion(0.5))
        
        self.play(Create(gr), run_time=1.5)
        self.play(FadeIn(red_dot), run_time=0.5)

        # Prop: planeta (la Tierra)
        tierra = Circle(radius=0.6, color=TEAL, fill_opacity=0.5, fill_color=TEAL)
        tierra.move_to(UP * 1.5 + RIGHT * 3)
        self.play(FadeIn(tierra), run_time=1.0)

        # Callout corto
        txt1 = Text("50 años intentando atraparla", color=ORANGE, font_size=36)
        txt1.move_to(DOWN * 2.5)
        self.play(FadeIn(txt1), run_time=0.8)
        
        self.wait(1)