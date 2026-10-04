from manim import *
from zenn_rig import *

class S10(Scene):
    def construct(self):
        titulo = titulo_seguro("¿CAMBIO DE IDENTIDAD?", color=INK)
        
        prota = protagonista(
            pos=LEFT * 2.6 + DOWN * 0.5,
            playera=BLUE,
            expresion="decidido",
            pose="brazos_cruzados"
        )
        
        contenedor = caja("PERSONALIDAD", pos=RIGHT * 2.2 + UP * 0.4, width=2.4)
        
        cruz = VGroup(
            Line(UP * 0.9 + LEFT * 0.9, DOWN * 0.9 + RIGHT * 0.9, stroke_width=12, color=RED),
            Line(UP * 0.9 + RIGHT * 0.9, DOWN * 0.9 + LEFT * 0.9, stroke_width=12, color=RED)
        ).move_to(contenedor.get_center())
        
        aviso_no = callout("¡NO!", color=RED, font_size=84).next_to(contenedor, DOWN, buff=0.45)

        self.play(
            FadeIn(titulo, shift=DOWN * 0.3),
            FadeIn(prota, shift=RIGHT * 0.4),
            FadeIn(contenedor, shift=LEFT * 0.4),
            run_time=1.0
        )
        
        self.play(
            Create(cruz),
            run_time=0.6
        )
        
        self.play(
            GrowFromCenter(aviso_no),
            run_time=0.5
        )
        
        self.wait(1.9)