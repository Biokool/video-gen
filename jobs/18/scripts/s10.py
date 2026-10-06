from manim import *
from zenn_rig import *

class S10(Scene):
    def construct(self):
        # Fondo nocturno
        self.add(fondo(INK))

        # Título superior (único en la escena)
        titulo = banda_titulo("Ritmo circadiano", color=YELLOW)
        self.play(FadeIn(titulo))
        self.wait(0.5)

        # Protagonista abajo a la izquierda
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 2.5,
            playera=PLAYERA_AZUL,
            altura=3.0,
            expresion="pensando",
            pose="de_pie",
        )
        self.play(FadeIn(prota))
        self.wait(0.5)

        # Luna y planeta en zona superior
        luna_obj = luna(pos=LEFT * 3 + UP * 2, radio=1.0, color=YELLOW, bg=INK)
        planeta_obj = planeta(pos=RIGHT * 2 + UP * 1, radio=0.95, color=TEAL)
        self.play(FadeIn(luna_obj), FadeIn(planeta_obj))
        self.wait(0.5)

        # Flecha del protagonista al planeta
        self.play(Create(arrow(prota.get_center(), planeta_obj.get_center())))
        self.wait(0.5)

        # Etiqueta con concepto clave (en lugar de callout, para evitar
        # un segundo "título" en la escena)
        etiqueta_insulina = etiqueta(
            "Insulina",
            planeta_obj.get_center() + UP * 0.6,
            color=ORANGE,
            font_size=40,
            ancho_max=5.5,
        )
        self.play(FadeIn(etiqueta_insulina))
        self.wait(1.5)

        # Cambia expresión a feliz
        cambiar_cara(prota, "feliz")
        self.wait(1)

        # Salida
        self.play(FadeOut(VGroup(prota, luna_obj, planeta_obj,
                                 etiqueta_insulina, titulo)))
        self.wait(0.5)