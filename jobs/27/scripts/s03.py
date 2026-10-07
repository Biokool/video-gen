from manim import *
from zenn_rig import *

class S03(Scene):
    def construct(self):
        # 1. Fondo de papel
        self.add(fondo_papel())

        # 2. Título de la escena
        titulo = titulo_seguro("El Universo Geocéntrico", color=INK)
        self.play(FadeIn(titulo, shift=UP * 0.3), run_time=0.5)

        # 3. Protagonista (a la izquierda, abajo de la zona de título)
        prota = protagonista(
            pos=DOWN * 1.1 + LEFT * 3.5,
            playera=PLAYERA_NARANJA,
            altura=2.4,
            expresion="pensando",
            pose="de_pie"
        )

        # 4. La Tierra y su órbita (a la derecha)
        earth_pos = RIGHT * 2.2 + DOWN * 0.5
        earth = planeta(pos=earth_pos, radio=0.7, color=TEAL)
        earth_label = etiqueta("Tierra (Inmóvil)", pos=earth_pos + DOWN * 1.1, font_size=30)
        
        orbit = Circle(radius=1.8, color=GRAY).set_opacity(0.4).shift(earth_pos)

        self.play(
            FadeIn(prota),
            FadeIn(earth),
            FadeIn(earth_label),
            Create(orbit),
            run_time=0.8
        )

        # 5. El Sol en su posición inicial (arriba de la Tierra)
        sun_start_pos = earth_pos + UP * 1.8
        sun = sol(color=YELLOW, radius=0.45, pos=sun_start_pos)
        sun_label = etiqueta("Sol", pos=sun_start_pos + UP * 0.6, font_size=30)

        self.play(
            FadeIn(sun),
            FadeIn(sun_label),
            run_time=0.6
        )
        self.wait(0.3)

        # 6. Animación del Sol girando alrededor de la Tierra
        sun_group = VGroup(sun)
        
        # Primera vuelta
        self.play(
            Rotate(sun_group, angle=2 * PI, about_point=earth_pos, run_time=2.5, rate_func=linear),
            FadeOut(sun_label, run_time=0.5)
        )

        # El protagonista cambia su expresión a confundido ante tal idea
        prota_confundido = protagonista(
            pos=DOWN * 1.1 + LEFT * 3.5,
            playera=PLAYERA_NARANJA,
            altura=2.4,
            expresion="confundido",
            pose="de_pie"
        )
        
        self.play(
            Transform(prota, prota_confundido),
            run_time=0.4
        )

        # El Sol continúa su órbita constante
        self.play(
            Rotate(sun_group, angle=PI, about_point=earth_pos, run_time=1.2, rate_func=linear)
        )
        self.wait(1.0)