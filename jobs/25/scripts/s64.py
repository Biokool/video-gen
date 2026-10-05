from manim import *
from zenn_rig import *

class S64(Scene):
    def construct(self):
        # Personaje principal con playera verde, expresión pensativa
        prota = protagonista(
            pos=LEFT * 3.5 + DOWN * 0.3,
            playera="verde",
            expresion="pensando",
            pose="de_pie"
        )

        # Ojo grande decorativo (símbolo de observación) a la derecha
        ojo = ojo_grande(
            pos=RIGHT * 3.5 + UP * 0.8,
            escala=1.0,
            iris=TEAL
        )

        # Libro abierto con dos páginas
        pag1 = pagina_calendario(width=1.7).rotate(-PI / 7)
        pag2 = pagina_calendario(width=1.7).rotate(PI / 7)
        libro = VGroup(pag1, pag2).move_to(ORIGIN + DOWN * 0.4)

        # Diagrama celular: curva con punto rojo, como figura del libro
        diagrama = curva(
            pos=libro.get_center() + UP * 0.15,
            ancho=2.4,
            alto=1.2,
            color=INK,
            acento=RED
        )

        # Entradas
        self.play(FadeIn(prota, shift=UP), run_time=1.0)
        self.play(FadeIn(ojo, shift=LEFT), run_time=0.8)
        self.play(FadeIn(libro, shift=UP), run_time=1.0)
        self.play(Create(diagrama), run_time=1.5)
        self.wait(0.5)

        # El personaje se acerca al libro para “estudiar”
        self.play(prota.animate.shift(RIGHT * 0.9), run_time=1.3)
        self.wait(0.4)

        # Se detiene y asiente con un pequeño movimiento
        self.play(prota.animate.shift(UP * 0.15), run_time=0.3)
        self.play(prota.animate.shift(DOWN * 0.15), run_time=0.3)

        # Regresa a su posición original
        self.play(prota.animate.shift(LEFT * 0.9), run_time=1.3)
        self.wait(1.0)