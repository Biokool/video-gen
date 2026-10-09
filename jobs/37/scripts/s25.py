from manim import *
from zenn_rig import *

class S25(Scene):
    def construct(self):
        # Fondo y título
        self.add(fondo_papel())
        banda = banda_titulo("Ópera a Cine", color=ORANGE)
        self.play(FadeIn(banda, shift=DOWN * 0.3), run_time=0.6)

        # Protagonista: posicionado abajo (y=-1.2) y con altura reducida (2.6) 
        # para evitar que su cabeza (y=1.4) choque con la banda (y=1.7)
        prota = version_prota(6, pos=DOWN * 1.2 + LEFT * 3.5, altura=2.6)
        self.play(FadeIn(prota, shift=UP * 0.5), run_time=0.8)

        # Props de la derecha
        casco = casco_vikingo(pos=RIGHT * 3.5 + UP * 0.8, escala=1.0)
        self.play(FadeIn(casco, scale=0.7), run_time=0.8)

        comic = caja("CÓMIC", pos=RIGHT * 3.5 + DOWN * 0.8, width=1.5)
        self.play(FadeIn(comic, shift=LEFT * 0.4), run_time=0.8)

        # Lupa y duplicación segura
        foco = lupa(pos=RIGHT * 0.5 + UP * 1.2, escala=1.2, color=INK)
        self.play(FadeIn(foco, scale=0.5), run_time=0.6)

        # Creamos una copia para el TransformFromCopy para evitar error de referencia circular
        foco2 = foco.copy().shift(RIGHT * 0.8)
        self.play(
            TransformFromCopy(foco, foco2),
            run_time=0.8
        )

        self.wait(1.0)

        # Limpieza de elementos para la siguiente transición
        self.play(
            FadeOut(casco),
            FadeOut(comic),
            FadeOut(foco),
            FadeOut(foco2),
            run_time=0.8
        )

        # Aparece el cine (oficina)
        cine = oficina(pos=RIGHT * 3.5 + UP * 0.2, size=1.6)
        self.play(FadeIn(cine, shift=UP * 0.4), run_time=0.8)

        self.wait(1.2)

        # Cierre de escena
        self.play(
            FadeOut(banda),
            FadeOut(prota),
            FadeOut(cine),
            run_time=0.8
        )