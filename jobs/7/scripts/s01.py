from manim import *
from zenn_rig import *

class S01(Scene):
    def construct(self):
        # VO: ¡Hola! Bienvenidos a El Porqué,
        # VISUAL: tarjeta_canal con el logo del canal.
        canal_card = tarjeta_canal()
        self.play(Create(canal_card, run_time=1.0))
        self.wait(2.0)

        # VO: donde cada video responde una pregunta que quizás nunca te habías hecho... pero deberías.
        # VISUAL: Protagonista (playera naranja, sonriendo) aparece al lado, saludando.
        self.play(FadeOut(canal_card, run_time=1.0))

        # El protagonista de la intro (versión 1) con playera naranja y expresión feliz por defecto.
        # Se posiciona a la izquierda para una buena composición.
        prota = version_prota(1, pos=LEFT*3.0)
        self.play(Create(prota, run_time=1.0))
        self.wait(4.0)