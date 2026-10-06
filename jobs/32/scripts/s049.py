from manim import *
from zenn_rig import *

class S049(Scene):
    def construct(self):
        # Protagonista (sin banda_titulo, ubicado abajo-izquierda)
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera="amarilla",
            altura=2.6,
            expresion="normal"
        )
        # Reloj con acento rojo (simula tachado)
        reloj = reloj_pared(pos=RIGHT*3 + UP*0.5, radius=1.0, hora_3=True)
        # Digitos (contador de horas) - nombre distinto para evitar sombra
        digitos_mob = digitos(pos=LEFT*3 + DOWN*1.5, size=0.9)

        self.play(FadeIn(prota), run_time=1)
        self.play(FadeIn(reloj), run_time=1)
        self.play(FadeIn(digitos_mob), run_time=1)
        self.wait(0.5)

        # Cambiar a expresión pensativa (reflexiva)
        prota_pensando = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera="amarilla",
            altura=2.6,
            expresion="pensando"
        )
        self.play(Transform(prota, prota_pensando), run_time=0.5)
        self.wait(0.5)

        # Acentuar el reloj con rojo (simular tachado)
        reloj_resaltado = red_accent(reloj, scale=1.25)
        self.play(Transform(reloj, reloj_resaltado), run_time=0.5)
        self.wait(0.5)

        # Flecha que señala del protagonista al reloj (indicando la hora)
        flecha = arrow(prota.get_right(), reloj.get_left(), color=INK, width=8)
        self.play(Create(flecha), run_time=0.8)
        self.wait(2)

        # Pausa final para cerrar la escena
        self.wait(1.5)