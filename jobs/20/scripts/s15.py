from manim import *
from zenn_rig import *

class S15(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        banda = banda_titulo("El consejo de la abuela", color=AZUL_MARINO)
        self.play(FadeIn(banda), run_time=0.8)

        prota = protagonista(LEFT * 3.8 + DOWN * 0.5, playera=AZUL_MARINO,
                             expresion='pensando', pose='de_pie')
        abuela = personaje(RIGHT * 3.4 + DOWN * 0.5, cuerpo=CORAL,
                           altura=2.6, expresion_tipo='feliz')
        self.play(FadeIn(prota, shift=RIGHT * 0.6),
                  FadeIn(abuela, shift=LEFT * 0.6), run_time=1.5)

        boca = etiqueta("tómate un respiro", (3.4, 2.3), color=ORANGE)
        flecha = arrow(ORIGIN + RIGHT * 3.4 + UP * 1.7,
                       ORIGIN + RIGHT * 3.4 + UP * 1.0, color=ORANGE)
        self.play(Write(boca), Create(flecha), run_time=1.2)

        self.play(Indicate(banda, color=YELLOW), run_time=0.8)
        self.wait(0.6)

        cambiar_cara(prota, 'confundido')
        self.play(prota.animate.shift(LEFT * 0.5), run_time=0.9)
        self.wait(1.2)