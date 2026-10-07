from manim import *
from zenn_rig import *


class S24(Scene):
    def construct(self):
        self.add(fondo(INK), estrellas(n=42, seed=7, color=WHITE))

        banda = banda_titulo("1687 · PRINCIPIA · GRAVEDAD", color=YELLOW)
        self.play(FadeIn(banda), run_time=0.6)

        prota = protagonista(DOWN*1.2+LEFT*4.0, playera="amarilla", altura=2.4,
                             expresion="sorpresa", pose="senalando")
        self.play(FadeIn(prota), run_time=0.7)

        tierra = planeta(RIGHT*3.8+DOWN*0.9, radio=0.95, color=TEAL)
        self.play(FadeIn(tierra), run_time=0.6)

        luna_obj = luna(pos=RIGHT*5.4+UP*0.6, radio=0.32, color=WHITE, bg=INK)
        self.play(FadeIn(luna_obj), run_time=0.6)

        manzana = Circle(radius=0.16, color=RED, fill_opacity=1).move_to(LEFT*3.2+UP*1.6)
        self.play(FadeIn(manzana), run_time=0.4)
        self.play(manzana.animate.move_to(LEFT*3.2+DOWN*0.7), run_time=1.1)

        dato = etiqueta("Una misma fuerza:\nmanzana y planetas",
                        pos=RIGHT*3.0+UP*2.0, color=YELLOW,
                        font_size=38, ancho_max=4.2)
        self.play(FadeIn(dato), run_time=0.6)

        self.play(Rotate(luna_obj, angle=-PI*0.9,
                         about_point=tierra.get_center()), run_time=2.2)
        cambiar_cara(prota, "mente_explotada")
        self.wait(2.0)