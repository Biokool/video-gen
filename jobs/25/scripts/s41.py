from manim import *
from zenn_rig import *

class S41(Scene):
    def construct(self):
        # Fondo cósmico
        self.add(fondo(INK))
        self.add(estrellas(42))

        # Protagonista (playera amarilla, expresión de misterio/pensando)
        prota = protagonista(
            LEFT * 3.5,
            playera='amarilla',
            altura=3.0,
            expresion='pensando',
            pose='de_pie'
        )
        self.play(FadeIn(prota, shift=UP * 0.3), run_time=0.6)

        # Ojo cósmico gigante a la derecha
        ojo = ojo_grande(RIGHT * 3.5, escala=1.5, iris=TEAL)
        self.play(Create(ojo), run_time=0.8)

        # Remolino de colores cósmicos en el centro
        colores = [MOSTAZA, CORAL, TEAL, YELLOW, ORANGE, RED]
        swirl = VGroup()
        for i in range(20):
            ang = i * 0.7
            rad = 0.3 + i * 0.15
            punto = Dot(
                radius=0.1,
                color=colores[i % len(colores)]
            ).move_to(rad * np.array([np.cos(ang), np.sin(ang), 0]))
            swirl.add(punto)
        self.play(
            LaggedStart(
                *[GrowFromCenter(d) for d in swirl],
                lag_ratio=0.07
            ),
            run_time=1.2
        )

        # Reacción del protagonista
        cambiar_cara(prota, 'sorpresa')
        self.play(prota.animate.shift(UP * 0.1), run_time=0.4)

        # Callout corto
        callout("Se pone raro...", color=MOSTAZA)
        self.wait(0.5)