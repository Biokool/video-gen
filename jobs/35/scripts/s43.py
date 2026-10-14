from manim import *
from zenn_rig import *

class S43(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.0,
            playera=PLAYERA_MORADA,
            altura=2.6,
            expresion="pensando",
            pose="de_pie"
        )
        
        titulo = titulo_seguro(
            "¿Naturaleza o Habilidad?",
            color=INK,
            font_size=52,
            y=2.5
        )
        
        nota = caja(
            etiqueta="PIANO",
            pos=RIGHT * 3.0 + DOWN * 0.5,
            width=2.5
        )
        
        interrogacion = etiqueta(
            "¿?",
            pos=RIGHT * 3.0 + UP * 1.2,
            color=ORANGE,
            font_size=60
        )
        
        flecha = arrow(
            start=prota.get_right() + UP * 0.5,
            end=nota.get_left(),
            color=INK,
            width=8
        )
        
        self.play(
            FadeIn(prota),
            FadeIn(titulo),
            run_time=1.0
        )
        
        self.play(
            FadeIn(nota),
            FadeIn(interrogacion),
            Create(flecha),
            run_time=1.0
        )
        
        cambiar_cara(prota, "sorpresa")
        
        self.wait(2.5)