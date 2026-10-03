from manim import *
from zenn_rig import *

class S06(Scene):
    def construct(self):
        self.add(fondo(INK))
        
        # Renombrar la variable para evitar conflicto con la función 'estrellas'
        grupo_estrellas = estrellas(20)
        self.add(grupo_estrellas)
        
        # Renombrar la variable 'luna' a 'luna_obj' para evitar conflicto con la función 'luna'
        luna_obj = luna(pos=UP * 3 + RIGHT * 4, radio=0.5, bg=INK)
        self.play(FadeIn(luna_obj), run_time=1.0)
        
        titulo = Text("1970: La Curva de Rotación", color=WHITE, font_size=56)
        self.play(FadeIn(titulo), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(titulo), run_time=0.5)
        
        fig = stick_idle(pos=LEFT * 3, height=2.2, color=WHITE)
        self.play(FadeIn(fig), run_time=1.0)
        expresion(fig, "preocupado")
        
        planeta = planeta(pos=ORIGIN, radio=1.5, color=YELLOW)
        self.play(FadeIn(planeta), run_time=1.5)
        
        halo = VGroup(
            Circle(radius=2.5, color=ORANGE, stroke_width=2, stroke_opacity=0.5),
            Circle(radius=3.5, color=ORANGE, stroke_width=2, stroke_opacity=0.3),
            Circle(radius=4.5, color=ORANGE, stroke_width=2, stroke_opacity=0.15)
        ).move_to(planeta)
        self.play(FadeIn(halo), run_time=2.0)
        
        curva = curva(pos=RIGHT * 2 + DOWN * 2, ancho=3, alto=2)
        self.play(FadeIn(curva), run_time=1.5)
        
        callout1 = callout("Velocidad constante", color=ORANGE, font_size=48)
        callout1.move_to(UP * 2 + RIGHT * 1)
        self.play(FadeIn(callout1), run_time=1.0)
        self.wait(1.0)
        
        self.play(FadeOut(callout1), run_time=0.5)
        
        stick_point(fig, planeta)
        self.wait(1.0)
        
        callout2 = callout("Masa invisible", color=YELLOW, font_size=48)
        callout2.move_to(DOWN * 2 + LEFT * 2)
        self.play(FadeIn(callout2), run_time=1.0)
        self.wait(1.0)
        
        reloj = clock_montage(radius=1.0)
        reloj.move_to(UP * 2.5 + LEFT * 3)
        self.play(FadeIn(reloj), run_time=1.5)
        self.wait(2.0)
        
        self.play(FadeOut(callout2), FadeOut(reloj), run_time=1.0)
        
        callout3 = callout("Halo de materia oscura", color=ORANGE, font_size=48)
        callout3.move_to(DOWN * 2.5)
        self.play(FadeIn(callout3), run_time=1.0)
        self.wait(2.0)
        
        self.play(
            FadeOut(callout3), 
            FadeOut(halo), 
            FadeOut(curva), 
            FadeOut(planeta), 
            FadeOut(fig), 
            FadeOut(luna_obj), 
            FadeOut(grupo_estrellas), 
            run_time=1.5
        )
        self.wait(0.5)