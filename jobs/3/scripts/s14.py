from manim import *
from zenn_rig import *

class S14(Scene):
    def construct(self):
        # Fondo espacial oscuro
        self.add(fondo(INK))
        estrellas_obj = estrellas(20)
        self.play(FadeIn(estrellas_obj), run_time=1.0)

        # Tarjeta de título inicial
        titulo = title_card("Lente Gravitacional", YELLOW)
        self.play(FadeIn(titulo), run_time=1.0)
        self.wait(0.5)
        self.play(FadeOut(titulo), run_time=0.5)

        # Split screen para mostrar la predicción y el concepto
        # Izquierda: Einstein (monigote) pensando
        einstein = stick_idle(ORIGIN + 2*LEFT, color=WHITE, height=2.0)
        self.play(FadeIn(einstein), run_time=0.5)
        expresion(einstein, "preocupado")  # Concentración científica
        
        # Derecha: Prop visual del fenómeno (planeta como lente)
        # Usamos una variable local con nombre diferente para evitar conflicto con la función
        obj_planeta = planeta(ORIGIN + 2*RIGHT + 0.5*UP, radio=0.8, color=TEAL)
        self.play(FadeIn(obj_planeta), run_time=0.5)
        
        # Estrella lejana (fuente de luz)
        estrella_fuente = sol()
        estrella_fuente.move_to(ORIGIN + 4*RIGHT + 1*UP)
        self.play(FadeIn(estrella_fuente), run_time=0.5)

        # Flecha que muestra la desviación
        flecha_luz = arrow(estrella_fuente.get_center(), ORIGIN + 2*RIGHT - 0.5*DOWN, color=YELLOW)
        self.play(Create(flecha_luz), run_time=1.0)

        # Callout principal
        callout1 = callout("1919: Einstein", color=YELLOW, font_size=72)
        callout1.to_edge(LEFT, buff=0.5)
        self.play(Write(callout1), run_time=1.0)

        # Einstein señala hacia el fenómeno
        stick_point(einstein, obj_planeta.get_center())
        
        self.wait(1.0)

        # Transición al concepto final
        self.play(FadeOut(callout1), FadeOut(flecha_luz), run_time=0.5)
        
        callout2 = callout("Lente Gravitacional", color=ORANGE, font_size=80)
        callout2.to_edge(DOWN, buff=0.5)
        self.play(Write(callout2), run_time=1.0)

        # Cambiar expresión a sorpresa/realización
        expresion(einstein, "sorpresa")
        
        self.wait(1.0)