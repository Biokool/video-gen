from manim import *
from zenn_rig import *

class S22(Scene):
    def construct(self):
        # 1. Setup: Fondo espacial oscuro
        self.add(fondo(INK))
        estrellas = estrellas(30)
        self.play(FadeIn(estrellas), run_time=1.0)

        # 2. Título corto de capítulo
        titulo = title_card("Masa Cósmica", color=YELLOW)
        self.play(FadeIn(titulo, scale=1.2), run_time=0.8)
        self.wait(0.5)
        self.play(FadeOut(titulo), run_time=0.5)

        # 3. Split Screen: Izquierda (Materia Oscura) vs Derecha (Materia Ordinaria)
        # Izquierda: Monigote con aura oscura/planeta
        fig_izq = stick_idle(pos=LEFT * 4, height=2.0, color=WHITE)
        planeta_oscuro = planeta(pos=LEFT * 4 + DOWN * 2.5, radio=0.8, color=INK)
        # Añadimos un borde para que se vea sobre fondo oscuro
        borde_planeta = Circle(radius=0.8, color=RED, stroke_width=2)
        borde_planeta.move_to(planeta_oscuro)
        
        # Derecha: Monigote "normal" con sol/materia ordinaria
        fig_der = stick_idle(pos=RIGHT * 4, height=2.0, color=YELLOW)
        sol_brig = sol()
        sol_brig.move_to(RIGHT * 4 + DOWN * 2.5)
        sol_brig.scale(0.8)

        self.play(
            FadeIn(fig_izq),
            FadeIn(fig_der),
            Create(planeta_oscuro),
            Create(borde_planeta),
            FadeIn(sol_brig),
            run_time=1.5
        )
        self.wait(0.5)

        # 4. Expresiones y Callouts
        # Expresión de sorpresa/realización en ambos
        self.play(
            expresion(fig_izq, "sorpresa"),
            expresion(fig_der, "sorpresa"),
            run_time=0.5
        )

        # Callout Izquierda: 95% Materia Oscura
        callout_izq = callout("95% Materia Oscura", color=RED, font_size=48)
        callout_izq.move_to(LEFT * 4 + UP * 2.5)
        
        # Callout Derecha: 100% Materia Ordinaria
        callout_der = callout("100% Materia Ordinaria", color=YELLOW, font_size=48)
        callout_der.move_to(RIGHT * 4 + UP * 2.5)

        self.play(
            Write(callout_izq),
            Write(callout_der),
            run_time=1.5
        )
        self.wait(0.5)

        # 5. Acciones: Señalar
        # El de la izquierda señala su planeta oscuro (su "masa" dominante)
        self.play(
            stick_point(fig_izq, planeta_oscuro),
            run_time=0.8
        )
        
        # El de la derecha señala su sol (su "ser" biológico)
        self.play(
            stick_point(fig_der, sol_brig),
            run_time=0.8
        )
        self.wait(0.5)

        # 6. Cierre: Transformación sutil para reforzar el contraste
        # Hacemos que el planeta oscuro pulse y el sol brille (escala)
        self.play(
            planeta_oscuro.animate.scale(1.1),
            borde_planeta.animate.scale(1.1),
            sol_brig.animate.scale(1.1),
            run_time=0.8
        )
        self.play(
            planeta_oscuro.animate.scale(1/1.1),
            borde_planeta.animate.scale(1/1.1),
            sol_brig.animate.scale(1/1.1),
            run_time=0.8
        )