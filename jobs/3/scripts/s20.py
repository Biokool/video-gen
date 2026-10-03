from manim import *
from zenn_rig import *

class S20(Scene):
    def construct(self):
        self.add(fondo(WHITE))
        
        # Título de la escena
        titulo = Text("¿Qué es la materia oscura?", font_size=48, color=INK)
        self.play(Write(titulo), run_time=1.0)
        self.wait(0.5)

        # Monigote científico
        sci = stick_idle(LEFT * 4, color=INK)
        self.play(FadeIn(sci), run_time=0.8)
        
        # Expresión de duda/pensamiento
        expresion(sci, "preocupado")
        self.wait(0.5)

        # Prop: Axión (partícula ligera)
        axion = planeta(ORIGIN + RIGHT * 2, 0.5, TEAL)
        axion_label = Text("Axiones", font_size=36, color=TEAL).next_to(axion, DOWN, buff=0.3)
        axion_group = VGroup(axion, axion_label)
        
        # Prop: WIMP (partícula pesada)
        wimp = planeta(ORIGIN + RIGHT * 5, 0.8, ORANGE)
        wimp_label = Text("WIMPs", font_size=36, color=ORANGE).next_to(wimp, DOWN, buff=0.3)
        wimp_group = VGroup(wimp, wimp_label)

        # Entrada de la primera partícula
        self.play(FadeIn(axion_group, shift=UP * 0.5), run_time=1.0)
        
        # Callout descriptivo para axiones
        callout_1 = callout("Muy ligeros y abundantes", color=TEAL, font_size=48)
        callout_1.to_edge(UP, buff=0.5)
        self.play(Write(callout_1), run_time=1.0)
        self.wait(1.0)
        
        # El científico señala los axiones
        stick_point(sci, axion.get_center())
        self.wait(0.5)
        self.play(FadeOut(callout_1), run_time=0.5)

        # Entrada de la segunda partícula
        self.play(FadeIn(wimp_group, shift=UP * 0.5), run_time=1.0)
        
        # Callout descriptivo para WIMPs
        callout_2 = callout("Más pesados", color=ORANGE, font_size=48)
        callout_2.to_edge(UP, buff=0.5)
        self.play(Write(callout_2), run_time=1.0)
        self.wait(1.0)

        # El científico señala los WIMPs
        stick_point(sci, wimp.get_center())
        self.wait(0.5)
        self.play(FadeOut(callout_2), run_time=0.5)

        # Cambio de expresión a sorpresa/misterio
        expresion(sci, "sorpresa")
        
        # Callout final de misterio
        callout_final = callout("Sigue siendo un misterio", color=RED, font_size=52)
        callout_final.move_to(ORIGIN)
        
        # Agrupamos las partículas para moverlas hacia arriba y dejar espacio
        particulas = VGroup(axion_group, wimp_group)
        self.play(
            particulas.animate.shift(UP * 2),
            FadeIn(callout_final),
            run_time=1.5
        )
        
        self.wait(1.0)
        
        # Salida
        self.play(
            FadeOut(titulo),
            FadeOut(sci),
            FadeOut(particulas),
            FadeOut(callout_final),
            run_time=1.0
        )