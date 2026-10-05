from manim import *
from zenn_rig import *

class S54(Scene):
    def construct(self):
        # Protagonista con playera amarilla
        prota = protagonista(
            pos=LEFT * 3 + DOWN * 0.4,
            playera='amarilla',
            altura=3.0,
            expresion='pensando',
            pose='de_pie'
        )
        self.play(FadeIn(prota, scale=0.85, run_time=1.0))
        self.wait(0.4)

        # Ojo gigante: la ciencia nos permite "ver"
        eye = ojo_grande(
            pos=RIGHT * 3.1 + DOWN * 0.2,
            escala=0.9,
            iris=YELLOW
        )
        self.play(FadeIn(eye, scale=0.6, run_time=1.0))
        self.wait(0.4)

        # Bombilla brillante sobre la cabeza
        bulb = sol(
            color=YELLOW,
            radius=0.35,
            pos=prota.get_top() + UP * 0.7
        )
        self.play(Create(bulb), run_time=0.8)

        # Expresión iluminada (cambio directo, sin self.play)
        cambiar_cara(prota, 'alegria_pura')
        self.wait(0.3)

        # Callout corto: "ver"
        word = callout('"ver"', color=YELLOW, font_size=72)
        word.to_corner(UR)
        word.shift(LEFT * 0.5 + DOWN * 0.5)
        self.play(FadeIn(word, scale=0.8), run_time=0.8)
        self.wait(0.8)