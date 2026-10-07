from manim import *
from zenn_rig import *

class S32(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=50))
        banda = banda_titulo("La corrección que cambió todo", color=YELLOW)
        self.play(FadeIn(banda), run_time=0.6)

        prota = protagonista(pos=DOWN*1.2 + LEFT*3.5, playera="rosa",
                             altura=2.6, expresion="alegria_pura", pose="de_pie")
        self.play(FadeIn(prota, shift=UP*0.3), run_time=0.6)

        centro = RIGHT*3.5 + UP*0.8
        sol_obj = sol(color=YELLOW, radius=0.7, pos=centro)
        tierra = planeta(pos=centro + RIGHT*1.8, radio=0.45, color=TEAL)
        self.play(FadeIn(sol_obj), FadeIn(tierra), run_time=0.6)

        orbita = Arc(radius=1.8, start_angle=0, angle=-PI*0.75, arc_center=centro)
        self.play(MoveAlongPath(tierra, orbita), run_time=2.5)

        nota = etiqueta("Física moderna y tecnología",
                        pos=RIGHT*3.4 + DOWN*1.6,
                        color=YELLOW, font_size=36, ancho_max=4.0)
        self.play(FadeIn(nota, shift=UP*0.2), run_time=0.6)
        self.wait(1.8)