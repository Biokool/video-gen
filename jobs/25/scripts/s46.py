from manim import *
from zenn_rig import *

class S46(MovingCameraScene):
    def construct(self):
        # Noche espacial
        self.add(fondo(INK))
        self.add(estrellas(n=42, seed=7, color=WHITE))

        # Protagonista con playera amarilla, pensando y señalando hacia la estrella
        prota = protagonista(
            pos=LEFT * 3.8,
            playera="amarilla",
            altura=3.0,
            expresion="pensando",
            pose="senalando"
        )
        self.play(FadeIn(prota, shift=UP * 0.5), run_time=0.7)

        # Próxima Centauri: enana roja distante
        estrella = sol(color=RED, radius=0.5, pos=RIGHT * 4.2)
        self.play(Create(estrella), run_time=0.7)

        # Ojo que observa hacia lo lejos
        ojo = ojo_grande(pos=RIGHT * 0.8, escala=0.6, iris=ORANGE)
        self.play(FadeIn(ojo, scale=0.6), run_time=0.7)

        # Pregunta corta en pantalla, lejos de subtítulos
        pregunta = callout("¿Qué vemos?", color=YELLOW, font_size=72)
        pregunta.to_edge(UP, buff=0.6)
        self.play(FadeIn(pregunta, scale=0.8), run_time=0.5)

        # Zoom hacia la estrella distante
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(estrella.get_center()),
            run_time=1.0
        )
        self.wait(0.3)