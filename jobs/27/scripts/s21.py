from manim import *
from zenn_rig import *

class S21(Scene):
    def construct(self):
        self.add(fondo(INK))
        banda = banda_titulo("Galileo, 1610", color=ORANGE)
        prota = protagonista(DOWN*1.5+LEFT*4, playera="roja", altura=2.4,
                             expresion="euforico", pose="senalando")
        ojo = ojo_grande(LEFT*1.2+UP*0.4, escala=1.1, iris=TEAL)
        venus = planeta(RIGHT*2.6+UP*1.2, radio=0.6, color=ORANGE)
        jupiter = planeta(RIGHT*4.8+UP*0.7, radio=0.8, color=CORAL)

        self.play(FadeIn(banda), FadeIn(prota), run_time=1.0)
        self.play(Create(ojo), FadeIn(venus), FadeIn(jupiter), run_time=1.0)
        self.play(Create(arrow(ojo.get_right(), venus.get_left(), color=YELLOW)),
                  run_time=0.8)

        nota = etiqueta("Fases de Venus y lunas de Júpiter",
                        RIGHT*2.5+DOWN*1.6, color=YELLOW, font_size=36,
                        ancho_max=5.0)
        self.play(FadeIn(nota), run_time=0.6)
        self.wait(1.8)

        self.play(FadeIn(red_accent(venus)), FadeIn(red_accent(jupiter)),
                  run_time=0.8)
        cambiar_cara(prota, "euforico")
        self.wait(2.0)