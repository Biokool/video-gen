from manim import *
from zenn_rig import *

class S33(Scene):
    def construct(self):
        self.add(fondo_papel())
        logo = etiqueta("EL PORQUÉ", (5.6, -1.8), color=TEAL, font_size=40, ancho_max=2.4)
        prota = protagonista(DOWN*1.3 + LEFT*3.6, PLAYERA_TEAL, altura=2.6,
                             expresion='feliz', pose='senalando')
        self.play(FadeIn(prota, shift=UP*0.4), FadeIn(logo, shift=UP*0.3), run_time=1.0)

        dato = callout("¡Nos vemos en el próximo video!", color=TEAL,
                       ancho_max=4.6, pos=RIGHT*3.4 + UP*1.3)
        self.play(FadeIn(dato, shift=LEFT*0.35), run_time=0.8)
        self.wait(1.2)

        cambiar_cara(prota, 'alegria_pura')
        self.wait(0.8)
        self.play(prota.animate.shift(UP*0.18), run_time=0.5)
        self.play(prota.animate.shift(DOWN*0.18), run_time=0.5)
        cambiar_cara(prota, 'feliz')
        self.wait(1.4)

        self.play(FadeOut(VGroup(prota, dato, logo)), run_time=0.8)