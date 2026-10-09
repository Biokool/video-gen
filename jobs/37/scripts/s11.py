from manim import *
from zenn_rig import *

class S11(Scene):
    def construct(self):
        # 1. Inicializar fondo de papel para estilo divulgación
        self.add(fondo_papel())

        # 2. Título superior seguro
        titulo = banda_titulo("¿Cascos con cuernos?", color=CORAL)
        self.play(FadeIn(titulo))

        # 3. Protagonista en zona segura (izquierda, abajo)
        prota = protagonista(
            pos=LEFT * 3.8 + DOWN * 1.1,
            playera="roja",
            altura=2.4,
            expresion="confundido",
            pose="de_pie"
        )
        self.play(FadeIn(prota))
        self.wait(1.5)

        # 4. Mostrar el casco vikingo en el lado derecho
        casco = casco_vikingo(pos=RIGHT * 3.5 + UP * 0.5, escala=1.3)
        self.play(Create(casco))
        self.wait(2.0)

        # 5. Línea de tiempo (camino) que representa el retroceso en el tiempo
        linea_tiempo = camino(width=5.0, pos=RIGHT * 0.5 + DOWN * 1.2)
        self.play(Create(linea_tiempo))
        self.wait(1.5)

        # Etiqueta indicando la verdadera época (Edad de Bronce)
        etiq_tiempo = etiqueta("Bronce: -1000 a.C.", pos=RIGHT * 0.5 + DOWN * 0.6, color=AZUL_MARINO)
        self.play(FadeIn(etiq_tiempo))
        self.wait(2.0)

        # 6. Reacción del protagonista ante el dato confuso
        cambiar_cara(prota, "mente_explotada")
        self.wait(1.0)

        # 7. Etiqueta aclaratoria de que fue mucho antes de los vikingos
        etiq_mito = etiqueta("¡Mucho antes!", pos=RIGHT * 3.5 + DOWN * 0.6, color=RED)
        self.play(FadeIn(etiq_mito))
        self.wait(4.0)