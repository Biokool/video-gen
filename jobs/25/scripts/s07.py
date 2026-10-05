from manim import *
from zenn_rig import *


class S07(Scene):
    """
    Escena 07 - "El porque de la vista".
    Correcciones aplicadas:
      - red_accent() / cambiar_cara() pueden devolver un Mobject (p. ej. Circle)
        en vez de un Animation: se envuelve con FadeIn antes de play() para que
        Scene.play() nunca reciba un Mobject suelto.
      - etiqueta() devuelve el texto creado: ahora se anyade a la escena
        (antes se descartaba y no se via).
      - Logica de reproduccion centralizada en _animar().
    """

    def _animar(self, resultado, run_time=0.4, **kw):
        """Reproduce un Animation; si devuelve un Mobject, lo anima con FadeIn."""
        if resultado is None:
            self.wait(max(run_time * 0.5, 0.2))
            return
        if isinstance(resultado, Animation):
            self.play(resultado, run_time=run_time, **kw)
        else:
            self.play(FadeIn(resultado), run_time=run_time, **kw)

    def construct(self):
        # ---------- Personaje principal (todas las escenas) ----------
        prota = protagonista(pos=LEFT * 3.2 + DOWN * 0.6, playera="azul",
                             altura=3.0, expresion='sorpresa', pose='senalando')

        # ---------- Elementos de la escena ----------
        ojo = ojo_grande(pos=RIGHT * 0.6 + UP * 0.1, escala=0.95, iris=TEAL)
        hormiga = dino(pos=RIGHT * 3.7 + DOWN * 0.3, color=INK, escala=0.32)
        flecha = arrow(RIGHT * 1.7 + UP * 0.05,
                       RIGHT * 3.25 + DOWN * 0.2, color=INK, width=8)

        et_cm = etiqueta("1 cm", (RIGHT * 2.5 + DOWN * 1.55),
                         color=RED, font_size=36)
        et_ant = etiqueta("HORMIGA", (RIGHT * 3.7 + UP * 1.35), font_size=32)

        call = callout("A UN CENTIMETRO!", ORANGE)

        # ---------- Animacion ----------
        self.add(prota)
        self.play(FadeIn(prota, shift=RIGHT), run_time=0.7)

        self.play(FadeIn(ojo), FadeIn(hormiga), run_time=0.6)

        # Etiquetas: se anyaden ahora (antes no se via)
        self.add(et_cm, et_ant)
        self.play(FadeIn(et_cm, scale=1.15), FadeIn(et_ant, scale=1.15),
                  run_time=0.45)

        # Flecha: se dibuja
        self.play(Create(flecha), run_time=0.6)

        # Acento rojo sobre la hormiga
        acento = red_accent(hormiga)
        self._animar(acento, run_time=0.3)
        self.wait(0.4)

        # Cambio de expresion
        cambio = cambiar_cara(prota, 'confundido')
        self._animar(cambio, run_time=0.4)

        self.wait(0.3)

        # Callout
        self.play(Write(call), run_time=0.5)
        self.wait(0.6)