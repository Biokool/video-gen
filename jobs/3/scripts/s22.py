from manim import *
from zenn_rig import *

def estrellas(n=50):
    """Crea un VGroup con n estrellas (pequeños círculos blancos) aleatorios."""
    stars = VGroup()
    for _ in range(n):
        star = Dot(
            np.random.uniform(-7, 7), 
            np.random.uniform(-4, 4), 
            color=WHITE,
            scale=0.1
        )
        stars.add(star)
    return stars

class S22(Scene):
    def construct(self):
        # Escenario nocturno/especial para "materia oscura"
        self.add(fondo(INK))
        
        # Estrellas de fondo
        estrellas_obj = estrellas(n=50)
        self.play(FadeIn(estrellas_obj, run_time=1.5))

        # Split screen: Lado Izquierdo (Cosmos/Materia Oscura)
        lado_izq = VGroup()
        fig_derecho = stick_idle(LEFT * 3, height=2.5, color=WHITE)
        expresion_derecho = expresion(fig_derecho, "sorpresa")
        
        # Elementos cósmicos abstractos para el lado izquierdo
        esfera_oscura = Esfera(radius=1.5, color=PURPLE_E, opacity=0.3)
        esfera_oscura.move_to(LEFT * 6 + UP * 1)
        
        lado_izq.add(fig_derecho, expresion_derecho, esfera_oscura)
        
        # Split screen visual divider
        linea_division = Line(UP*4, DOWN*4, color=WHITE, stroke_width=2)
        self.play(Create(linea_division))
        
        # Lado Derecho (Biología/Materia Ordinaria)
        fig_izquierdo = stick_idle(RIGHT * 3, height=2.5, color=YELLOW)
        expresion_izquierdo = expresion(fig_izquierdo, "normal")
        
        # Prop biológico: ADN simplificado o célula (usamos una esfera brillante)
        celula = Circle(radius=1.2, color=GREEN_E, fill_opacity=0.5)
        celula.move_to(RIGHT * 6 + UP * 1)
        
        self.add(fig_izquierdo, expresion_izquierdo, celula)

        # Transición: El personaje de la derecha se acerca al centro para explicar
        self.play(fig_izquierdo.animate.next_to(linea_division, RIGHT, buff=0.5),
                  expresion_izquierdo.animate.next_to(fig_izquierdo, UP))
        
        # Callout principal: "95% Materia Oscura"
        callout_1 = callout("95% MATERIA OSCURA", color=PURPLE_E)
        callout_1.move_to(LEFT * 6 + DOWN * 2.5)
        
        self.play(FadeIn(callout_1))
        self.wait(3)

        # Cambio de expresión a "sorpresa" en el personaje de la derecha para enfatizar
        self.play(Transform(expresion_izquierdo, expresion(fig_izquierdo, "miedo")))
        
        # Callout 2: "100% Materia Ordinaria"
        callout_2 = callout("100% MATERIA ORDINARIA", color=GREEN_E)
        callout_2.move_to(RIGHT * 6 + DOWN * 2.5)
        
        self.play(FadeIn(callout_2))
        
        # Animación final: Los dos grupos se miran
        self.play(fig_derecho.animate.look_at(fig_izquierdo),
                  fig_izquierdo.animate.look_at(fig_derecho))
        
        self.wait(3)