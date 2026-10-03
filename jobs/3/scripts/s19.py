from manim import *
from zenn_rig import *

class S19(Scene):
    def construct(self):
        # Fondo de noche/espacio
        self.add(fondo(INK))
        est = estrellas(40)
        self.play(FadeIn(est), run_time=1.5)

        # Título de la escena
        tit = title_card("MOND", YELLOW)
        self.play(FadeIn(tit), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(tit), run_time=0.8)

        # Monigotes
        grupo = stick_group(3, pos=ORIGIN, height=2.0, color=WHITE)
        self.play(FadeIn(grupo[0]), FadeIn(grupo[1]), FadeIn(grupo[2]), run_time=1.5)

        # Prop: curva de rotación (gráfica con punto rojo)
        graf = curva(pos=RIGHT * 3 + UP * 1, ancho=3, alto=2)
        self.play(Create(graf), run_time=1.5)

        # Expresión preocupada en el primer monigote
        expresion(grupo[0], "preocupado")
        self.wait(1.0)

        # Callout: MOND
        co1 = callout("MOND", color=YELLOW, font_size=72)
        co1.to_edge(UP, buff=0.5)
        self.play(FadeIn(co1), run_time=0.8)
        self.wait(1.5)

        # El segundo monigote señala la curva
        stick_point(grupo[1], graf)
        self.wait(1.0)

        # Callout: falla en CMB y lentes
        co2 = callout("¿CMB y lentes?", color=ORANGE, font_size=64)
        co2.next_to(co1, DOWN, buff=0.3)
        self.play(FadeIn(co2), run_time=0.8)
        self.wait(1.5)

        # Expresión triste en todos
        for fig in grupo:
            expresion(fig, "triste")
        self.wait(1.0)

        # El tercer monigote piensa
        stick_think(grupo[2], "¿Gravedad incompleta?")
        self.wait(1.5)

        # Apagar estrellas y salir
        self.play(
            FadeOut(co1),
            FadeOut(co2),
            FadeOut(graf),
            FadeOut(grupo[0]),
            FadeOut(grupo[1]),
            FadeOut(grupo[2]),
            run_time=1.2
        )
        self.play(FadeOut(est), run_time=0.8)
        self.wait(0.5)