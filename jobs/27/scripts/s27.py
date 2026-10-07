from manim import *
from zenn_rig import *

class S27(Scene):
    def construct(self):
        banda = banda_titulo("La longitud en alta mar", color=YELLOW)
        self.play(FadeIn(banda, shift=DOWN * 0.3), run_time=0.8)

        prota = protagonista(DOWN * 1.4 + LEFT * 3.6, PLAYERA_AMARILLA, altura=2.6,
                             expresion='alegria_pura', pose='senalando')
        barco = personaje(RIGHT * 2.0 + DOWN * 1.5, AZUL_MARINO, altura=2.0,
                          expresion_tipo='feliz')
        instr = lupa(RIGHT * 4.2 + DOWN * 0.5, escala=0.8)
        lab = etiqueta("sextante", (4.2, -1.85), color=AZUL_MARINO)
        pez1 = pez(RIGHT * 5.9 + DOWN * 1.9, CORAL, escala=0.9)

        self.play(FadeIn(prota, shift=UP * 0.3),
                  FadeIn(barco, shift=RIGHT * 0.4),
                  FadeIn(instr), FadeIn(lab), FadeIn(pez1),
                  run_time=1.0)

        flecha = arrow(LEFT * 1.6 + UP * 0.3, RIGHT * 0.6 + UP * 0.3, color=ORANGE)
        self.play(Create(flecha),
                  barco.animate.shift(RIGHT * 0.7),
                  instr.animate.shift(RIGHT * 0.7),
                  lab.animate.shift(RIGHT * 0.7),
                  pez1.animate.shift(LEFT * 0.5),
                  run_time=1.6)

        dato = etiqueta("Precisión: ~1.5 km", (3.4, 1.4), color=ORANGE)
        self.play(FadeIn(dato, scale=0.9), run_time=1.0)
        self.wait(1.0)