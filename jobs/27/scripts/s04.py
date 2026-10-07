from manim import *
from zenn_rig import *

class S04(Scene):
    def construct(self):
        # Fondo crema cálido de papel
        self.add(fondo_papel())

        # Título superior seguro
        titulo = banda_titulo("Un siglo de retraso", color=CORAL)

        # Protagonista en la esquina inferior izquierda (zona segura)
        prota = protagonista(
            pos=DOWN * 1.2 + LEFT * 3.5,
            playera=PLAYERA_NARANJA,
            altura=2.5,
            expresion="triste"
        )

        # Elementos que representan el tiempo y los avances (calendario y reloj)
        cal = calendario(pos=RIGHT * 0.2 + DOWN * 1.0, width=1.8)
        reloj = reloj_pared(pos=RIGHT * 3.2 + DOWN * 1.0, radius=0.9)
        etiq = etiqueta("Avances perdidos", pos=(1.7, 1.2))

        # Entrada de escena
        self.play(
            FadeIn(titulo),
            FadeIn(prota)
        )
        self.wait(0.5)

        # Aparecen los avances científicos y de navegación
        self.play(
            Create(cal),
            Create(reloj),
            Write(etiq)
        )
        self.wait(1.0)

        # El tiempo se desvanece y se bloquea el avance
        accent = red_accent(reloj, scale=1.3)
        
        # Cambiamos la cara en el acto antes de la animación
        cambiar_cara(prota, "enojado")
        
        self.play(
            FadeOut(cal, shift=DOWN),
            Create(accent),
            run_time=1.5
        )
        self.wait(1.5)