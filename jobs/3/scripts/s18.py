from manim import *
from zenn_rig import *

class S18(Scene):
    def construct(self):
        # Fondo oscuro espacial
        self.add(fondo(INK))
        estrellas = estrellas(30)
        self.play(FadeIn(estrellas), run_time=1.0)

        # Título de sección
        titulo = title_card("Búsqueda Sin Éxito", color=YELLOW)
        self.play(FadeIn(titulo), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(titulo), run_time=0.8)

        # Monigote principal (físico preocupado)
        fig = stick_idle(pos=ORIGIN + 2*LEFT + 0.5*DOWN, height=2.2, color=WHITE)
        self.play(FadeIn(fig), run_time=1.0)

        # Cara de preocupación
        cara = expresion(fig, "preocupado")
        self.play(FadeIn(cara), run_time=0.5)

        # Reloj de pared (pasaje del tiempo sin resultados)
        reloj = reloj_pared()
        reloj.move_to(3*RIGHT + 2*UP)
        self.play(Create(reloj), run_time=1.0)

        # Caja vacía (materia oscura no detectada)
        caja = caja("0 partículas", pos=2*RIGHT + DOWN)
        self.play(FadeIn(caja), run_time=1.0)

        # Flecha del monigote hacia la caja vacía
        flecha = arrow(fig.get_center() + 0.5*RIGHT, caja.get_center())
        self.play(Create(flecha), run_time=0.8)

        # Callout corto
        call = callout("Sin detección", color=ORANGE, font_size=72)
        call.to_edge(UP, buff=0.5)
        self.play(Write(call), run_time=1.2)
        self.wait(1.0)

        # El monigote señala la caja
        self.play(stick_point(fig, caja), run_time=1.0)
        self.wait(0.5)

        # Montaje de reloj (pasaje del tiempo)
        montage = clock_montage(radius=1.2)
        montage.move_to(ORIGIN + 1*DOWN)
        self.play(FadeIn(montage), run_time=1.2)
        self.wait(1.5)

        # Cambio de expresión a tristeza (frustración)
        self.play(Transform(cara, expresion(fig, "triste")), run_time=0.8)
        self.wait(1.0)

        # Limpieza final
        self.play(FadeOut(call), run_time=0.8)
        self.play(FadeOut(flecha), run_time=0.5)
        self.play(FadeOut(montage), run_time=0.8)
        self.play(FadeOut(caja, reloj, fig, cara), run_time=1.0)
        self.play(FadeOut(estrellas), run_time=0.8)
        self.remove(fondo(INK))