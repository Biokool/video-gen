from manim import *
from zenn_rig import *

class S04(Scene):
    def construct(self):
        # Protagonista con playera naranja y expresión pensativa
        prota = protagonista(
            pos=LEFT * 4 + DOWN * 0.5,
            playera=PLAYERA_NARANJA,
            altura=3.0,
            expresion='pensando',
            pose='de_pie'
        )
        self.play(FadeIn(prota))
        self.wait(0.5)

        # Cerebro estilizado
        brain_color = GREY_BROWN
        stroke_color = GREY_D
        brain_scale = 1.0

        # Lóbulos principales del cerebro
        lobe_left = Ellipse(width=2.5 * brain_scale, height=1.8 * brain_scale, color=brain_color, fill_opacity=0.9, stroke_width=4, stroke_color=stroke_color)
        lobe_right = Ellipse(width=2.3 * brain_scale, height=1.7 * brain_scale, color=brain_color, fill_opacity=0.9, stroke_width=4, stroke_color=stroke_color)
        
        # Agrupar y posicionar los lóbulos ligeramente superpuestos
        brain_body = VGroup(lobe_left.shift(LEFT * 0.6 * brain_scale), lobe_right.shift(RIGHT * 0.6 * brain_scale))
        brain_body.move_to(RIGHT * 3)

        # Detalles de circunvoluciones (líneas curvas)
        conv_color = GREY_D
        conv_width = 3
        brain_center_pos = brain_body.get_center()

        # --- FIX: CubicBezier requiere 4 puntos (start, control1, control2, end) ---
        # Se asume que los 3 puntos originales definían un punto de inicio, un punto "pico"
        # que actúa como control principal, y un punto final. Se generan los dos puntos
        # de control para la curva cúbica interpolando desde los extremos hacia el pico.

        # Convolución 1 (superior)
        p1_start = brain_center_pos + LEFT * 0.9 * brain_scale + UP * 0.4 * brain_scale
        p1_peak = brain_center_pos + UP * 0.7 * brain_scale
        p1_end = brain_center_pos + RIGHT * 0.9 * brain_scale + UP * 0.4 * brain_scale
        conv1 = CubicBezier(
            p1_start,
            interpolate(p1_start, p1_peak, 0.7), # control_point_1
            interpolate(p1_end, p1_peak, 0.7),   # control_point_2
            p1_end,
            stroke_color=conv_color, stroke_width=conv_width
        )

        # Convolución 2 (inferior)
        p2_start = brain_center_pos + LEFT * 0.8 * brain_scale + DOWN * 0.3 * brain_scale
        p2_peak = brain_center_pos + DOWN * 0.6 * brain_scale
        p2_end = brain_center_pos + RIGHT * 0.8 * brain_scale + DOWN * 0.3 * brain_scale
        conv2 = CubicBezier(
            p2_start,
            interpolate(p2_start, p2_peak, 0.7), # control_point_1
            interpolate(p2_end, p2_peak, 0.7),   # control_point_2
            p2_end,
            stroke_color=conv_color, stroke_width=conv_width
        )

        # Convolución 3 (izquierda vertical)
        p3_start = brain_center_pos + LEFT * 0.3 * brain_scale + UP * 0.1 * brain_scale
        p3_peak = brain_center_pos + LEFT * 0.1 * brain_scale
        p3_end = brain_center_pos + LEFT * 0.3 * brain_scale + DOWN * 0.1 * brain_scale
        conv3 = CubicBezier(
            p3_start,
            interpolate(p3_start, p3_peak, 0.7), # control_point_1
            interpolate(p3_end, p3_peak, 0.7),   # control_point_2
            p3_end,
            stroke_color=conv_color, stroke_width=conv_width
        )

        # Convolución 4 (derecha vertical)
        p4_start = brain_center_pos + RIGHT * 0.3 * brain_scale + UP * 0.1 * brain_scale
        p4_peak = brain_center_pos + RIGHT * 0.1 * brain_scale
        p4_end = brain_center_pos + RIGHT * 0.3 * brain_scale + DOWN * 0.1 * brain_scale
        conv4 = CubicBezier(
            p4_start,
            interpolate(p4_start, p4_peak, 0.7), # control_point_1
            interpolate(p4_end, p4_peak, 0.7),   # control_point_2
            p4_end,
            stroke_color=conv_color, stroke_width=conv_width
        )
        # --- FIN FIX ---
        
        brain_details = VGroup(conv1, conv2, conv3, conv4)
        brain = VGroup(brain_body, brain_details)

        self.play(Create(brain), run_time=1.5)

        # Líneas rítmicas que irradian del cerebro
        rhythm_lines = VGroup()
        for i in range(6): # 6 líneas radiales
            line = Line(ORIGIN, RIGHT * 0.8, color=TEAL, stroke_width=4)
            line.rotate(i * PI / 3, about_point=ORIGIN)
            rhythm_lines.add(line)
        rhythm_lines.move_to(brain.get_center())

        self.add(rhythm_lines.set_opacity(0)) # Añadir las líneas invisibles inicialmente

        # Animación de vibración rítmica (5 segundos)
        # Cada ciclo de animación dura 1 segundo (0.5s de crecimiento, 0.5s de encogimiento)
        for _ in range(5):
            self.play(
                AnimationGroup(
                    LaggedStart(*[line.animate.set_opacity(1).scale(1.2, about_point=brain.get_center()) for line in rhythm_lines], lag_ratio=0.05),
                    brain.animate.scale(1.02).set_color(GREY_A), # Pulso sutil del cerebro
                    run_time=0.5
                ),
                AnimationGroup(
                    LaggedStart(*[line.animate.set_opacity(0).scale(1/1.02, about_point=brain.get_center()) for line in rhythm_lines], lag_ratio=0.05),
                    brain.animate.scale(1/1.02).set_color(brain_color), # Regresar al estado normal
                    run_time=0.5
                )
            )

        self.wait(0.5) # Pausa final