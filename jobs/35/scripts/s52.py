from manim import *
from zenn_rig import *

class S52(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título seguro arriba (solo una llamada a título/banda)
        self.add(banda_titulo("¡MÁXIMA EFICIENCIA!", color=ORANGE))
        
        # Protagonista abajo a la izquierda (evita banda y zona de subtítulos)
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.8,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="mente_explotada",
            pose="senalando"
        )
        
        # Prop con color a la derecha
        m = matraz(pos=RIGHT * 3.2 + DOWN * 0.5, escala=1.2, liquido=TEAL)
        
        # Usar etiqueta en lugar de callout para evitar llamadas redundantes de texto destacado
        c = etiqueta("¡300% MÁS RÁPIDO!", pos=RIGHT * 3.2 + UP * 1.5, color=RED, font_size=40)
        
        self.play(
            FadeIn(prota),
            FadeIn(m),
            FadeIn(c),
            run_time=1.0
        )
        
        cambiar_cara(prota, "alegria_pura")
        self.wait(2.5)