"""Escena S01 corregida y autónoma.

Esta versión elimina la dependencia de ``zenn_rig`` y define
funciones locales para crear el título, el monigote y sus
animaciones. Así evitamos pasar objetos que no son animaciones a
``Scene.play`` (el error original: *Unexpected argument Circle passed
to Scene.play*).

Ejecutar con, por ejemplo:
    manim -pqh script.py S01
"""

from manim import *
from manim.utils.space_ops import angle_of_vector  # <-- necesario para calcular ángulos


# ----------------------------------------------------------------------
# Utilidades de dibujo
# ----------------------------------------------------------------------


def title_card(text: str, *, color: str = YELLOW) -> Text:
    """Devuelve un ``Text`` grande para usar como título."""
    return Text(text, color=color, font_size=72)


def stick_idle(position: np.ndarray = ORIGIN, *, height: float = 2.2, color: str = WHITE) -> VGroup:
    """Crea un monigote sencillo (cabeza + cuerpo + brazos + piernas)."""
    # Proporciones básicas
    head_radius = height * 0.1
    body_len = height * 0.4
    arm_len = height * 0.2
    leg_len = height * 0.3
    leg_spread = height * 0.2

    # Cabeza
    head = Circle(radius=head_radius, color=color, fill_opacity=1).move_to(
        position + UP * (height * 0.9)
    )

    # Cuerpo
    body = Line(
        start=head.get_bottom(),
        end=head.get_bottom() + DOWN * body_len,
        color=color,
    )

    # Brazos (a la altura de la cintura)
    arm_y = body.get_start() + UP * (body_len * 0.5)
    left_arm = Line(start=arm_y, end=arm_y + LEFT * arm_len, color=color)
    right_arm = Line(start=arm_y, end=arm_y + RIGHT * arm_len, color=color)

    # Piernas
    leg_start = body.get_end()
    left_leg = Line(
        start=leg_start,
        end=leg_start + LEFT * leg_spread + DOWN * leg_len,
        color=color,
    )
    right_leg = Line(
        start=leg_start,
        end=leg_start + RIGHT * leg_spread + DOWN * leg_len,
        color=color,
    )

    stick = VGroup(head, body, left_arm, right_arm, left_leg, right_leg)
    stick.move_to(position)          # centrado en la posición solicitada
    return stick


def stick_walk(stick: VGroup, target: np.ndarray, *, run_time: float = 5) -> Animation:
    """Animación que lleva al monigote a ``target``."""
    anim = stick.animate.move_to(target)
    anim.set_run_time(run_time)
    return anim


def stick_point(stick: VGroup, direction: np.ndarray) -> Animation:
    """
    Hace que el brazo derecho apunte en ``direction``.
    Se rota el brazo alrededor de su punto de origen.
    """
    # En nuestro VGroup, el brazo derecho es el cuarto elemento (índice 3)
    right_arm = stick[3]
    # Ángulo deseado respecto al eje X
    target_angle = angle_of_vector(direction)
    # Ángulo actual del brazo
    current_angle = right_arm.get_angle()
    # Rotación necesaria
    delta = target_angle - current_angle
    return right_arm.animate.rotate(delta, about_point=right_arm.get_start())


def stick_think(stick: VGroup, text: str) -> VGroup:
    """
    Crea una burbuja de pensamiento con ``text`` situada encima del monigote.
    Se usa un ``RoundedRectangle`` como burbuja y se añade un pequeño círculo
    como "cola".
    """
    # Burbuja principal
    bubble = RoundedRectangle(
        corner_radius=0.2,
        height=0.9,
        width=2.2,
        fill_color=WHITE,
        fill_opacity=0.9,
        stroke_color=BLACK,
    ).next_to(stick, UP, buff=0.4)

    # Pequeña "cola" de la burbuja
    tail = Circle(radius=0.07, fill_color=WHITE, fill_opacity=0.9, stroke_color=BLACK)
    tail.move_to(bubble.get_bottom() + DOWN * 0.07 + LEFT * 0.2)

    # Texto dentro de la burbuja
    txt = Text(text, font_size=24, color=BLACK).move_to(bubble.get_center())

    return VGroup(bubble, tail, txt)


# ----------------------------------------------------------------------
# Escena principal
# ----------------------------------------------------------------------


class S01(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # Título breve
        # ------------------------------------------------------------------
        title = title_card("Galaxia Lejana", color=YELLOW)
        self.play(FadeIn(title, scale=0.8))
        self.wait(2)
        self.play(FadeOut(title))

        # ------------------------------------------------------------------
        # Monigote quieto a la izquierda
        # ------------------------------------------------------------------
        stick = stick_idle(LEFT * 3, height=2.2, color=WHITE)
        self.play(FadeIn(stick, scale=0.8))
        self.wait(2)

        # ------------------------------------------------------------------
        # Caminar lentamente al centro
        # ------------------------------------------------------------------
        target = RIGHT * 2
        self.play(stick_walk(stick, target, run_time=5))
        self.wait(1)

        # ------------------------------------------------------------------
        # Señalar hacia arriba (las estrellas)
        # ------------------------------------------------------------------
        self.play(stick_point(stick, UP * 2))
        self.wait(1.5)

        # ------------------------------------------------------------------
        # Pensar con burbuja corta
        # ------------------------------------------------------------------
        thought = stick_think(stick, "¿Por qué no se escapan?")
        self.play(FadeIn(thought, scale=0.8))
        self.wait(3)

        # ------------------------------------------------------------------
        # Salida
        # ------------------------------------------------------------------
        self.play(FadeOut(stick), FadeOut(thought))
        self.wait(2)