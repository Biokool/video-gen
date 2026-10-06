from manim import *
from zenn_rig import *

class S025(Scene):
    def construct(self):
        # Protagonista
        prota = protagonista(pos=ORIGIN, playera="verde", altura=3.0, expresion='sorpresa', pose='de_pie')
        # Callout con el dato
        dato = callout(text="1%")
        dato.move_to(UP*2)
        # Etiqueta con el aumento de latidos
        latido = etiqueta("+3-5 lpm", pos=(0, -1), color=INK, font_size=40, ancho_max=5.5)
        # Acento rojo al latido
        latido_ac = red_accent(latido, scale=1.25)

        # Animaciones
        self.play(FadeIn(prota), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(dato), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(latido), run_time=1.0)
        self.wait(0.5)
        self.play(Create(latido_ac), run_time=0.5)
        self.wait(0.5)
        self.play(prota.animate.shift(UP*0.2), run_time=0.5)
        self.wait(0.3)
        self.play(prota.animate.shift(DOWN*0.2), run_time=0.5)
        self.wait(4.5)  # completar ~13 segundos totales