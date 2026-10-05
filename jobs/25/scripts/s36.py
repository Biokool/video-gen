from manim import *
from zenn_rig import *

class S36(Scene):
    def construct(self):
        # Protagonista "EL PORQUÉ" con playera rosa y expresión de asombro
        por = protagonista(LEFT*3.5, playera='rosa', expresion='sorpresa', pose='de_pie')
        self.play(FadeIn(por))
        self.wait(0.5)

        # Ojo gigante: la ciencia que mira lo invisible
        ojo = ojo_grande(ORIGIN, escala=1.2, iris=TEAL)
        self.play(Create(ojo), run_time=1.5)
        self.wait(0.3)

        # Doble hélice de ADN
        dna = VGroup()
        for idx, phase in enumerate([0, PI]):
            dna.add(ParametricFunction(
                lambda t, p=phase: np.array([0.6*np.sin(2*t + p), t, 0]),
                t_range=[-1.5, 1.5],
                color=TEAL if idx == 0 else ORANGE
            ))
        rungs = VGroup()
        for y in np.linspace(-1.0, 1.0, 5):
            left = np.array([0.6*np.sin(2*y), y, 0])
            right = np.array([0.6*np.sin(2*y + PI), y, 0])
            rungs.add(Line(left, right, stroke_width=2, color=WHITE))
        dna.add(rungs)
        dna.move_to(RIGHT*3.2)
        self.play(Create(dna), run_time=2)
        self.wait(0.3)

        # Estructuras de proteínas (glóbulos y lazos)
        proteina = VGroup(
            Circle(radius=0.4, color=AZUL_MARINO, fill_opacity=0.8),
            Circle(radius=0.3, color=CORAL, fill_opacity=0.8).shift(UP*0.5),
            Circle(radius=0.35, color=CREMA, fill_opacity=0.8).shift(DOWN*0.6),
            Line(np.array([0.4, 0, 0]), np.array([0, 0.5, 0]), color=INK),
            Line(np.array([0, 0.5, 0]), np.array([-0.4, 0.3, 0]), color=INK),
            Line(np.array([0.4, 0, 0]), np.array([0.3, -0.4, 0]), color=INK),
        )
        proteina.next_to(dna, DOWN, buff=0.6)
        self.play(FadeIn(proteina, shift=UP*0.3), run_time=1)
        self.wait(0.3)

        # Flecha del ojo al ADN: "estamos viendo"
        flecha = arrow(ojo.get_right(), dna.get_left(), color=INK, width=8)
        self.play(Create(flecha), run_time=1)
        self.wait(0.3)

        # Etiquetas discretas y seguras
        etiqueta("ADN", (dna.get_center()[0], dna.get_top()[1] + 0.4))
        etiqueta("proteínas", (proteina.get_center()[0], proteina.get_top()[1] + 0.4))

        # Cambio a expresión feliz al final
        cambiar_cara(por, 'feliz')
        self.wait(1)