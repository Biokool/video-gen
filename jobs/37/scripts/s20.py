from manim import *
from zenn_rig import *

class S20(Scene):
    def construct(self):
        # Fondo de papel cálido
        self.add(fondo_papel())

        # Título superior seguro
        title = banda_titulo("¿Cuernos en la batalla?", ORANGE)
        self.play(FadeIn(title))

        # Guerrero (monigote) con casco de vikingo en el lado izquierdo
        warrior = stick_idle(pos=LEFT * 2.6 + DOWN * 1.1, height=2.2, color=INK)
        helmet = casco_vikingo(pos=LEFT * 2.6 + UP * 0.15, escala=0.8)
        self.play(FadeIn(warrior), FadeIn(helmet))

        # Protagonista observando en el lado derecho (fuera de la zona de subtítulos)
        prota = protagonista(
            pos=RIGHT * 2.6 + DOWN * 1.2,
            playera="naranja",
            altura=2.4,
            expresion="pensando",
            pose="de_pie",
        )
        self.play(FadeIn(prota))

        # El guerrero piensa en el impedimento y se añade una etiqueta de duda
        thought = stick_think(warrior, "¡Se atora!")
        # La etiqueta se coloca al lado CONTRARIO del protagonista (a la izquierda)
        lbl = etiqueta(
            "¿Poco práctico?",
            LEFT * 2.6 + UP * 1.0,
            color=INK,
        )
        self.play(FadeIn(thought), FadeIn(lbl))

        # Acento rojo sobre el casco para enfatizar el problema del diseño
        accent = red_accent(helmet, scale=1.4)
        # red_accent devuelve un VGroup; usar FadeIn en vez de Create
        self.play(FadeIn(accent))

        # El protagonista cambia su expresión al comprender el absurdo
        # cambiar_cara actúa directamente, no devuelve una animación
        cambiar_cara(prota, "sorpresa")
        self.wait(1.5)