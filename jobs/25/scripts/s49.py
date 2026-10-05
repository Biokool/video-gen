from manim import *
from zenn_rig import *

class S49(Scene):
    def construct(self):
        # Fondo espacial
        self.add(fondo(INK), estrellas(n=42, seed=7, color=WHITE))

        # Protagonista con playera amarilla, mirando con asombro
        prota = protagonista(
            pos=np.array([-3.7, -0.8, 0]),
            playera="amarilla",
            altura=2.8,
            expresion="sorpresa",
            pose="de_pie"
        )
        self.play(FadeIn(prota), run_time=0.8)

        # Galaxia espiral majestuosa
        galaxia = self.crear_galaxia(np.array([4.2, 0.3, 0]))
        self.play(Create(galaxia), run_time=2.2)
        self.wait(0.5)

        # La cabeza le explota de grandeza
        cambiar_cara(prota, "mente_explotada")
        self.wait(0.6)

        # Ojo grande que enfatiza la maravilla
        ojo = ojo_grande(pos=np.array([0.0, 2.1, 0]), escala=0.9)
        self.play(FadeIn(ojo), run_time=0.8)
        self.wait(2.5)

    def crear_galaxia(self, pos):
        # Núcleo brillante
        nucleo = Circle(
            radius=0.35,
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(pos)

        # Dos brazos espirales (logarítmicos)
        brazo1 = ParametricFunction(
            lambda t: pos + np.array([
                0.25 * t * np.cos(5.5 * t),
                0.25 * t * np.sin(5.5 * t),
                0
            ]),
            t_range=[0.6, 6.2],
            color=WHITE,
            stroke_width=2.5,
        )
        brazo2 = ParametricFunction(
            lambda t: pos + np.array([
                0.25 * t * np.cos(5.5 * t + PI),
                0.25 * t * np.sin(5.5 * t + PI),
                0
            ]),
            t_range=[0.6, 6.2],
            color=LIGHT_BROWN,
            stroke_width=2.5,
        )

        # Polvo estelar alrededor
        estrellas_galaxia = VGroup()
        for _ in range(22):
            ang = np.random.uniform(0, TAU)
            radio = np.random.uniform(0.6, 2.4)
            punto = pos + np.array([
                radio * np.cos(ang),
                radio * np.sin(ang),
                0
            ])
            dot = Dot(punto, radius=0.02, color=WHITE)
            dot.set_opacity(np.random.uniform(0.4, 1.0))
            estrellas_galaxia.add(dot)

        gal = VGroup(nucleo, brazo1, brazo2, estrellas_galaxia)
        gal.scale(1.2)
        return gal