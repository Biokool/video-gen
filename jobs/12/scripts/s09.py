from manim import *
from zenn_rig import *

class S09(Scene):
    def construct(self):
        # 1. Configuración del fondo oscuro para misterio/ciencia
        self.add(fondo(AZUL_MARINO))
        
        # 2. Título superior seguro
        titulo = banda_titulo("EL SEXTO SENTIDO", color=CORAL)
        self.play(FadeIn(titulo))
        
        # 3. Personaje a la izquierda con los ojos cerrados ("dormido")
        sujeto = stick_idle(pos=LEFT * 3 + DOWN * 0.5, color=WHITE)
        cara_cerrada = expresion(sujeto, "dormido")
        cerebro_label = etiqueta("Cerebro", pos=LEFT * 3 + UP * 1.2, color=CREMA, font_size=32)
        
        self.play(
            FadeIn(sujeto),
            FadeIn(cara_cerrada),
            Write(cerebro_label),
            run_time=1.5
        )
        self.wait(1.5)
        
        # 4. Aparece el ojo misterioso en el centro-derecha (percepción espacial)
        ojo = ojo_grande(pos=RIGHT * 2.5 + UP * 0.5, escala=1.3, iris=CORAL)
        self.play(Create(ojo), run_time=1.0)
        self.wait(1.0)
        
        # 5. El sujeto se sorprende al "ver" con la mente y señala al ojo
        nuevo_sujeto = stick_point(sujeto, ojo.get_left())
        cara_sorpresa = expresion(nuevo_sujeto, "sorpresa")
        
        self.play(
            Transform(sujeto, nuevo_sujeto),
            Transform(cara_cerrada, cara_sorpresa),
            run_time=1.5
        )
        self.wait(0.5)
        
        # 6. Aparece la pregunta de investigación (Callout) debajo del ojo
        pregunta = callout("¿CÓMO FUNCIONA?", color=MOSTAZA, font_size=48)
        pregunta.move_to(RIGHT * 2.5 + DOWN * 1.4)
        
        self.play(FadeIn(pregunta), run_time=1.0)
        
        acento = red_accent(pregunta, scale=1.15)
        self.play(Create(acento), run_time=1.0)
        
        # 7. Tiempo de espera final para la narración completa
        self.wait(5.5)