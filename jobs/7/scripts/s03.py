from manim import *
from zenn_rig import *
import numpy as np # Importamos numpy para operaciones con vectores
import random # Importamos el módulo random para números aleatorios

class S03(Scene):
    def construct(self):
        # El protagonista "El Porqué" en su playera naranja, con expresión de asombro,
        # señalando hacia el espacio donde representaremos el pensamiento.
        el_porque = protagonista(
            pos=LEFT * 3,
            playera=PLAYERA_NARANJA,
            expresion='sorpresa',
            pose='senalando',
            altura=3.0
        )

        # Para representar el "cerebro" o la mente abstracta, utilizamos un matraz,
        # simbolizando un recipiente de ideas o un objeto de estudio científico.
        cerebro_metafora = matraz(
            pos=RIGHT * 2.5,
            escala=1.2,
            liquido=TEAL # Un líquido que sugiere actividad o esencia
        )

        # Destellos de luz abstractos para representar pensamientos y percepciones.
        # Se crean como un grupo de puntos alrededor del matraz.
        destellos_pensamiento = VGroup(*[
            Dot(
                # Generamos un vector aleatorio 3D y lo normalizamos para obtener una dirección unitaria.
                # np.random.uniform(-1, 1, 3) crea un array de 3 elementos con valores entre -1 y 1.
                random_vec = np.random.uniform(-1, 1, 3),
                # Calculamos la norma del vector para normalizarlo.
                norm = np.linalg.norm(random_vec),
                # Evitamos la división por cero si el vector es [0,0,0] (muy improbable, pero seguro).
                random_unit_vec = random_vec / norm if norm != 0 else np.array([0., 0., 1.]),
                # Multiplicamos por una magnitud aleatoria dentro del rango deseado.
                position_offset = random_unit_vec * random.uniform(0.3, 0.8),
                # Calculamos la posición final del punto.
                point=cerebro_metafora.get_center() + position_offset,
                radius=0.08,
                color=YELLOW
            )
            for _ in range(8)
        ])

        # Callout con el texto de la narración, posicionado en la parte superior
        # para evitar la zona de subtítulos.
        narracion_callout = callout("Ser tú, percibir, pensar.", color=ORANGE, font_size=64)
        narracion_callout.move_to(UP * 2.5)

        # --- Secuencia de Animación ---

        # 1. Introducción: Aparece el protagonista y la representación de la mente.
        self.play(
            FadeIn(el_porque),
            FadeIn(cerebro_metafora),
            run_time=1.0
        )

        # 2. Manifestación del pensamiento: Los destellos aparecen y el callout se muestra.
        self.play(
            Create(destellos_pensamiento, lag_ratio=0.2), # Los destellos aparecen escalonadamente
            FadeIn(narracion_callout),
            run_time=1.5
        )
        self.wait(1.0) # Mantenemos la escena para asimilar la idea

        # 3. Énfasis en el concepto de la mente.
        self.play(
            red_accent(cerebro_metafora), # Se resalta el matraz
            run_time=0.7
        )
        self.wait(0.5) # Pequeña pausa después del acento

        # 4. Salida: Todos los elementos se desvanecen.
        self.play(
            FadeOut(el_porque),
            FadeOut(cerebro_metafora),
            FadeOut(destellos_pensamiento),
            FadeOut(narracion_callout),
            run_time=1.0
        )