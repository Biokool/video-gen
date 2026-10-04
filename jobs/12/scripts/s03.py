from manim import *
from zenn_rig import *

class S03(Scene):
    def construct(self):
        # Título y división de pantalla
        banda = banda_titulo("¿Cuántos sentidos tenemos?", color=AZUL_MARINO)
        split = split_screen("Visión Clásica", "Ciencia Moderna", divider_color=INK)
        
        self.play(FadeIn(banda), FadeIn(split))
        self.wait(1.0)
        
        # Aristóteles (Gris, izquierda)
        aristoteles = stick_idle(pos=LEFT * 3.5 + DOWN * 0.5, color=GRAY)
        ari_exp = expresion(aristoteles, "normal")
        label_5 = callout("5", color=CORAL).scale(0.8).next_to(aristoteles, UP, buff=0.4)
        
        self.play(
            Create(aristoteles),
            FadeIn(ari_exp),
            Write(label_5),
            run_time=1.5
        )
        self.wait(1.5)
        
        # Científico moderno (Multicolor, derecha)
        cientifico = personaje(pos=RIGHT * 3.5 + DOWN * 0.5, cuerpo=TEAL, altura=2.4, expresion_tipo="feliz")
        label_12 = callout("12+", color=MOSTAZA).scale(0.8).next_to(cientifico, UP, buff=0.4)
        
        self.play(
            Create(cientifico),
            Write(label_12),
            run_time=1.5
        )
        
        # Énfasis en el "12+"
        accent = red_accent(label_12, scale=1.3)
        self.play(FadeIn(accent))
        self.wait(0.5)
        
        # Aristóteles se sorprende al saber que son más de 12
        ari_sorpresa = expresion(aristoteles, "sorpresa")
        self.play(Transform(ari_exp, ari_sorpresa), run_time=0.8)
        self.wait(2.2)