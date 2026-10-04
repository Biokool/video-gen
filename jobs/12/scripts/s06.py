from manim import *
from zenn_rig import *

class S06(Scene):
    def construct(self):
        # fondo nocturno
        self.add(fondo(INK))

        # monigote pensativo (izquierda)
        thinker = stick_idle(pos=LEFT * 3, height=2.2, color=WHITE)
        self.play(FadeIn(thinker, run_time=0.8))
        self.play(FadeIn(expresion(thinker, "preocupado"), run_time=0.5))
        self.play(FadeIn(stick_think(thinker, "?"), run_time=0.6))

        # mapa antiguo (derecha) simulado con caja etiquetada
        ancient_map = caja("Mapa", pos=RIGHT * 3, width=3)
        self.play(FadeIn(ancient_map, run_time=0.8))

        # flecha señalando del monigote al mapa
        arrow_to_map = arrow(thinker.get_center(), ancient_map.get_center(),
                             color=INK, width=8)
        self.play(FadeIn(arrow_to_map, run_time=0.5))

        # llamado breve en pantalla
        note = callout("Sin número mágico", color=ORANGE, font_size=96)
        self.play(FadeIn(note, run_time=0.7))

        # pausa para la narración
        self.wait(3)

        # resaltado rojo sobre el mapa
        self.play(FadeIn(red_accent(ancient_map), run_time=0.5))
        self.wait(2)

        # salida
        self.play(FadeOut(thinker), FadeOut(ancient_map),
                  FadeOut(arrow_to_map), FadeOut(note), run_time=1)