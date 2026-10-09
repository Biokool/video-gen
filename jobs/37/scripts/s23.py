from manim import *
from zenn_rig import *

class S23(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas())
        self.add(luna(pos=UP*2.5+RIGHT*4, radio=0.8, color=YELLOW, bg=INK))
        banda = banda_titulo("La verdad...", color=ORANGE)
        self.play(FadeIn(banda, shift=DOWN*0.4), run_time=0.8)
        prota = protagonista(pos=DOWN*1.2+LEFT*3.2, playera="naranja", altura=2.4, expresion="sorpresa", pose="senalando")
        self.play(FadeIn(prota, shift=UP*0.3), run_time=0.8)
        self.wait(0.4)
        cambio = Text("La cultura popular\nnos engaña", font_size=46, color=RED)
        cambio.move_to(UP*0.3+RIGHT*1.5)
        self.play(Write(cambio), run_time=1.0)
        self.wait(0.4)
        self.play(Create(Line(cambio.get_left()+LEFT*0.2, cambio.get_right()+RIGHT*0.2, color=RED, stroke_width=8)), run_time=0.6)
        self.wait(0.6)
        self.play(FadeOut(cambio), run_time=0.5)
        self.wait(0.2)