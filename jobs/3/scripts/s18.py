from manim import *

class S18(Scene):
    def construct(self):
        # Crear elementos básicos que existan en Manim core
        # Reemplazamos las funciones de zenn_rig por equivalentes o simples
        
        # Fondo
        fondo = Rectangle(
            width=16, height=9,
            color=BLACK,
            stroke_width=0
        )
        self.add(fondo)
        
        # Estrellas simples
        estrellas_obj = VGroup(*[
            Dot(radius=0.05, color=WHITE)
            for _ in range(20)
        ])
        estrellas_obj.arrange_in_grid(4, 5, buff=0.5)
        self.play(FadeIn(estrellas_obj), run_time=1.5)
        self.wait(0.5)
        
        # Montaje de reloj - usar un círculo simple como representación
        mont = Circle(radius=3.5, color=YELLOW)
        self.play(FadeIn(mont, scale=0.8), run_time=1.5)
        self.wait(1.0)
        
        # Figura de palo - usar un círculo como cabeza
        fig = Circle(radius=0.5, color=WHITE)
        fig.move_to(LEFT * 4.5)
        self.play(FadeIn(fig), run_time=1.0)
        
        # Expresión - texto simple
        expr = Text("preocupado", font_size=36)
        expr.next_to(fig, DOWN, buff=0.5)
        self.play(FadeIn(expr), run_time=0.8)
        self.wait(1.0)
        
        # Dinosaurio - usar un texto simple
        dino = Text("Dino", color=TEAL, font_size=48)
        dino.move_to(RIGHT * 4.5)
        self.play(FadeIn(dino), run_time=1.0)
        self.wait(1.0)
        
        # Callout - texto con fondo
        call_text = Text("Sin partículas detectadas", color=ORANGE, font_size=48)
        call = SurroundingRectangle(call_text, color=ORANGE, buff=0.2)
        call.add(call_text)
        call.to_edge(UP, buff=0.6)
        self.play(FadeIn(call, shift=DOWN * 0.3), run_time=1.0)
        self.wait(2.0)
        
        self.play(
            FadeOut(call),
            FadeOut(dino),
            run_time=1.5,
        )
        self.wait(1.0)
        
        self.play(
            FadeOut(fig),
            FadeOut(expr),
            FadeOut(mont),
            FadeOut(estrellas_obj),
            run_time=1.5,
        )