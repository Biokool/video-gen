from manim import *
from zenn_rig import *

class S18(Scene):
    def construct(self):
        # Fondo cálido estilo papel de divulgación
        self.add(fondo_papel())
        
        # Título superior seguro
        titulo = banda_titulo("¿Uso Ritual o de Batalla?", color=ORANGE)
        self.add(titulo)
        
        # Protagonista en el lado izquierdo señalando (con altura segura de 2.5)
        prota = version_prota(4, pos=DOWN * 1.2 + LEFT * 3.5, altura=2.5)
        
        # Props del lado derecho
        # Objeto Ritual: Vela
        objeto_ritual = vela(pos=RIGHT * 1.5 + DOWN * 0.5, escala=1.3)
        etiqueta_ritual = etiqueta("Ritual", pos=RIGHT * 1.5 + UP * 0.8, color=INK)
        
        # Objeto de Guerra: Casco Vikingo
        objeto_guerra = casco_vikingo(pos=RIGHT * 4.5 + DOWN * 0.5, escala=1.3)
        etiqueta_guerra = etiqueta("Guerra", pos=RIGHT * 4.5 + UP * 0.8, color=INK)
        
        # Animación secuencial
        self.play(FadeIn(prota))
        self.wait(0.5)
        
        # Aparece la opción ritual
        self.play(
            FadeIn(objeto_ritual),
            Write(etiqueta_ritual),
            run_time=1.0
        )
        self.wait(0.8)
        
        # Aparece la opción de guerra
        self.play(
            FadeIn(objeto_guerra),
            Write(etiqueta_guerra),
            run_time=1.0
        )
        self.wait(0.5)
        
        # El protagonista cambia de expresión y se descarta la opción de guerra
        cambiar_cara(prota, "sarcastico")
        acento_descarte = red_accent(objeto_guerra, scale=1.4)
        
        self.play(
            Create(acento_descarte),
            run_time=1.0
        )
        self.wait(1.5)