from manim import *
from zenn_rig import *

class S26(Scene):
    def construct(self):
        # Protagonista con playera celeste (usamos azul) y expresión pensativa
        prota = protagonista(LEFT * 2.2, playera="azul", altura=3.0,
                             expresion="pensando", pose="de_pie")
        self.play(FadeIn(prota, shift=DOWN), run_time=0.8)

        # Ojo grande como símbolo de percepción
        ojo = ojo_grande(RIGHT * 3.5, escala=0.9, iris=TEAL)
        self.play(Create(ojo), run_time=0.8)

        # Función local para construir engranajes (ruedas dentadas)
        def hacer_engranaje(pos, radio=0.45, color=GREY):
            dientes = VGroup()
            for i in range(10):
                ang = i * TAU / 10
                d = Rectangle(width=0.14, height=0.22, fill_color=color,
                              fill_opacity=0.7, stroke_width=0.5)
                d.move_to(pos + radio * UP).rotate(ang, about_point=pos)
                dientes.add(d)
            cuerpo = Circle(radius=radio, color=color, fill_opacity=0.7,
                            stroke_width=1).move_to(pos)
            return VGroup(cuerpo, dientes)

        # Engranajes: uno sobre la cabeza, otro más abajo (reconfigurándose)
        g1 = hacer_engranaje(prota.get_top() + UP * 0.4, radio=0.45, color=GREY)
        g2 = hacer_engranaje(prota.get_center() + UP * 1.4, radio=0.35, color=DARK_GREY)

        self.play(Create(g1), Create(g2), run_time=1.0)
        self.wait(0.2)

        # Giran en sentidos opuestos
        self.play(
            Rotate(g1, angle=TAU, run_time=1.5),
            Rotate(g2, angle=-TAU, run_time=1.5),
        )

        # Reconfiguración: los engranajes se intercambian de zona
        g1.generate_target()
        g1.target.move_to(g2.get_center() + UP * 1.1)
        g2.generate_target()
        g2.target.move_to(prota.get_top() + UP * 0.6)

        # Cambio de expresión a esfuerzo decidido
        cambiar_cara(prota, "decidido")

        self.play(
            MoveToTarget(g1, run_time=1.2),
            MoveToTarget(g2, run_time=1.2),
        )
        self.play(Rotate(g1, angle=PI / 2), Rotate(g2, angle=-PI / 2),
                  run_time=0.6)
        self.wait(0.5)