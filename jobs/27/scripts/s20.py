from manim import *
from zenn_rig import *

class S20(Scene):
    def construct(self):
        self.add(fondo(INK))
        self.add(estrellas(n=48, seed=3, color=WHITE))
        banda = banda_titulo("Solo un ejercicio matemático", color=ORANGE)
        self.play(FadeIn(banda), run_time=0.8)
        self.wait(0.5)
        prota = protagonista(DOWN * 1.6 + LEFT * 4.0, playera="roja",
                             altura=2.6, expresion="sarcastico",
                             pose="brazos_cruzados")
        astro = personaje(DOWN * 1.8 + RIGHT * 2.6, cuerpo=AZUL_MARINO,
                          altura=2.4, expresion_tipo='normal')
        self.play(FadeIn(prota, shift=UP * 0.4),
                  FadeIn(astro, shift=UP * 0.4), run_time=1.0)
        dato = etiqueta("¿Y la física?", pos=RIGHT * 4.0 + UP * 1.4,
                        color=ORANGE, font_size=40)
        self.play(FadeIn(dato, scale=0.8), run_time=0.8)
        self.wait(0.5)
        cambiar_cara(prota, "confundido")
        self.play(astro.animate.rotate(-0.05, about_point=astro.get_bottom()),
                  run_time=0.8)
        self.play(astro.animate.rotate(0.05, about_point=astro.get_bottom()),
                  run_time=0.8)
        self.wait(1.5)