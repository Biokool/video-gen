from manim import *
from zenn_rig import *

class S01(Scene):
    def construct(self):
        # Fondo nocturno y estrellas
        self.add(fondo(INK))
        self.add(estrellas(n=42, seed=7, color=WHITE))

        # Protagonista (conductor) – versión 1: naranja, de pie, feliz
        prota = version_prota(1)          # posición por defecto = ORIGIN
        self.play(FadeIn(prota), run_time=1.2)
        self.wait(0.5)

        # Luna
        luna_obj = luna(pos=UP * 2 + RIGHT * 3, radio=1.0, color=YELLOW, bg=INK)
        self.play(FadeIn(luna_obj), run_time=1.5)
        self.wait(0.5)

        # Monigote secundario (stick figure)
        stick = stick_idle(pos=LEFT * 2, height=2.2, color=WHITE)
        self.play(FadeIn(stick), run_time=1.0)
        expresion(stick, "feliz")
        self.wait(0.3)

        # Ojo grande
        eye = ojo_grande(pos=LEFT * 2 + UP * 1, escala=1.2)
        self.play(FadeIn(eye), run_time=0.8)
        self.wait(0.5)

        # Tarjeta del canal (única tarjeta/título por escena)
        self.play(FadeIn(tarjeta_canal()), run_time=1.0)
        self.wait(0.2)

        # Saludo usando una etiqueta (en lugar de callout)
        saludo = etiqueta(
            texto="¡Hola! Bienvenidos",
            pos=UP * 2.5,               # posición visible sobre la escena
            color=ORANGE,
            font_size=40,
            ancho_max=5.5,
        )
        self.play(FadeIn(saludo), run_time=1.2)
        self.wait(1)