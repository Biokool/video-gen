from manim import *
from zenn_rig import *

class S12(Scene):
    def construct(self):
        # 1. Fondo de papel cálido
        self.add(fondo_papel())

        # 2. Título seguro en la parte superior
        banda = banda_titulo("EDAD DEL BRONCE NÓRDICA", color=CORAL)
        self.play(Create(banda), run_time=1.0)

        # 3. Elementos de la escena
        # Protagonista a la izquierda señalando el descubrimiento
        prota = protagonista(
            pos=DOWN * 1.3 + LEFT * 4.0,
            playera="azul",
            altura=2.4,
            expresion="sorpresa",
            pose="senalando"
        )

        # Elemento central: Calendario que representa la época antigua
        cal = calendario(pos=LEFT * 0.3 + DOWN * 0.6, width=1.7)
        lbl = etiqueta("1200 - 1000 a.C.", pos=(-0.3, 0.8), color=INK)

        # Elemento derecho: El casco con cuernos real (tocado ceremonial)
        helmet = casco_vikingo(pos=RIGHT * 3.4 + DOWN * 0.6, escala=1.5)

        # 4. Animación secuencial
        self.play(
            FadeIn(prota, shift=RIGHT),
            run_time=1.2
        )
        
        self.play(
            Create(cal),
            Write(lbl),
            run_time=1.5
        )

        self.play(
            FadeIn(helmet, shift=UP),
            run_time=1.2
        )

        # Conexión visual: Flecha indicadora y acento rojo de destacar
        flecha = arrow(start=LEFT * 2.3 + DOWN * 0.4, end=RIGHT * 2.0 + DOWN * 0.4, color=INK)
        acento = red_accent(helmet, scale=1.3)

        self.play(
            Create(flecha),
            Create(acento),
            run_time=1.5
        )

        # Espera final para completar la narración (~10 segundos en total)
        self.wait(3.6)