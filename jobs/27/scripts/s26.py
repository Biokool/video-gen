from manim import *
from zenn_rig import *


class S26(Scene):
    def construct(self):
        self.add(fondo_papel())
        banda = banda_titulo("PREDECIR EL CIELO", color=MOSTAZA)
        self.play(FadeIn(banda, shift=DOWN * 0.3), run_time=0.7)

        prota = protagonista(DOWN * 1.5 + LEFT * 3.9, playera="amarilla",
                             altura=2.4, expresion="sorpresa", pose="senalando")
        self.play(FadeIn(prota, shift=UP * 0.3), run_time=0.8)

        reloj = reloj_pared(radius=1.0, pos=UP * 1.1)
        self.play(Create(reloj), run_time=1.0)
        self.play(Rotate(reloj, angle=0.4, rate_func=there_and_back), run_time=0.8)
        self.wait(0.4)

        marca = digitos(RIGHT * 4.2 + DOWN * 0.9, size=1.0)
        self.play(FadeIn(marca, scale=0.7), run_time=0.8)

        # red_accent puede devolver una Animation o un Mobject (p. ej. un Circle).
        # Si devuelve un Mobject, hay que envolverlo en una animación antes de
        # pasarlo a self.play().
        acento = red_accent(marca)
        if isinstance(acento, Animation):
            self.play(acento, run_time=0.9)
        else:
            self.play(FadeIn(acento, scale=0.6), run_time=0.6)
            self.wait(0.3)
            self.play(FadeOut(acento), run_time=0.4)

        dato = etiqueta("minutos \u2192 menos de 1 segundo",
                        RIGHT * 4.1 + UP * 1.3, color=CORAL)
        self.play(FadeIn(dato, shift=LEFT * 0.4), run_time=0.8)

        flecha = arrow(LEFT * 3.0 + DOWN * 0.6, RIGHT * 3.0 + DOWN * 0.6,
                       color=AZUL_MARINO)
        self.play(Create(flecha), run_time=0.7)
        self.wait(0.8)