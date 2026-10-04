from manim import *
from zenn_rig import *


class S05(Scene):
    def engranaje(self, color, r=0.4):
        cuerpo = Circle(radius=r, color=INK, stroke_width=4,
                        fill_color=color, fill_opacity=0.95)
        dirs = [UP, DOWN, LEFT, RIGHT, UP + LEFT, UP + RIGHT, DOWN + LEFT, DOWN + RIGHT]
        dientes = VGroup(*[
            Line((r * 0.9) * d / np.linalg.norm(d), (r * 1.35) * d / np.linalg.norm(d),
                 color=INK, stroke_width=4)
            for d in dirs
        ])
        hueco = Circle(radius=r * 0.32, color=INK, stroke_width=3,
                       fill_color=WHITE, fill_opacity=1).move_to(cuerpo)
        return VGroup(dientes, cuerpo, hueco)

    def bombilla(self, pos, encendida=False):
        foco = Circle(radius=0.42, color=INK, stroke_width=5,
                      fill_color=YELLOW, fill_opacity=0.85 if encendida else 0.05)
        rosca = Rectangle(width=0.32, height=0.22, color=INK, stroke_width=4,
                          fill_color=INK, fill_opacity=1).next_to(foco, DOWN, buff=0.03)
        rayos = VGroup(*[
            Line(0.6 * d / np.linalg.norm(d), 0.95 * d / np.linalg.norm(d),
                 color=YELLOW, stroke_width=6)
            for d in [UP, UP + LEFT, UP + RIGHT, LEFT, RIGHT]
        ])
        return VGroup(rayos, rosca, foco).move_to(pos)

    def construct(self):
        titulo = banda_titulo("NI MILAGRO... NI NADA", ORANGE)
        prota = protagonista(LEFT * 3.8 + DOWN * 0.5, PLAYERA_NARANJA, 3.0, 'pensando', 'de_pie')
        self.play(FadeIn(titulo, shift=DOWN * 0.3), FadeIn(prota, shift=UP * 0.3), run_time=1.0)

        aviso = callout("¿MILAGRO?", ORANGE, font_size=70)
        self.play(FadeIn(aviso, scale=1.1), run_time=0.5)
        self.wait(0.7)
        self.play(FadeOut(aviso), run_time=0.4)

        izq = Circle(radius=0.72, color=INK, stroke_width=5).shift(LEFT * 0.6)
        der = Circle(radius=0.72, color=INK, stroke_width=5).shift(RIGHT * 0.6)
        giros = VGroup(*[
            Arc(radius=0.38, start_angle=a, angle=PI * 0.85, color=INK, stroke_width=4)
            .shift(RIGHT * x + UP * y)
            for a, x, y in [(0.3, -0.6, 0.2), (1.9, 0.6, -0.1), (4.4, 0.05, 0.45)]
        ])
        eng1 = self.engranaje(ORANGE, 0.42).shift(RIGHT * 0.15 + DOWN * 0.05)
        eng2 = self.engranaje(TEAL, 0.28).shift(LEFT * 0.95 + UP * 0.45)
        cerebro = VGroup(izq, der, giros, eng1, eng2).shift(RIGHT * 2.6 + UP * 0.55)

        self.play(Create(cerebro), run_time=1.2)
        self.wait(0.3)

        flecha = arrow(prota.get_right() + UP * 0.6, cerebro.get_left() + DOWN * 0.3)
        self.play(Create(flecha), run_time=0.6)

        bombilla = self.bombilla(RIGHT * 3.6 + UP * 2.4, encendida=False)
        self.play(FadeIn(bombilla, scale=0.4), run_time=0.6)
        cambiar_cara(prota, 'sorpresa')
        self.play(Transform(bombilla, self.bombilla(RIGHT * 3.6 + UP * 2.4, encendida=True)),
                  run_time=0.6)
        self.play(Flash(bombilla, color=YELLOW, line_length=0.4, flash_radius=1.0), run_time=0.6)

        nota = etiqueta("engranajes en marcha", (2.6, -1.6), color=TEAL)
        acento = red_accent(bombilla)
        self.play(FadeIn(nota, shift=UP * 0.2), FadeIn(acento), run_time=0.6)
        self.wait(1.1)
        self.play(FadeOut(nota), FadeOut(acento), FadeOut(flecha), run_time=0.5)
        self.wait(0.4)