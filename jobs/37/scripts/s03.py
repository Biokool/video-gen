from manim import *
from zenn_rig import *

class S03(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título superior seguro
        banda = banda_titulo("EL MITO VIKINGO", color=AZUL_MARINO)
        self.play(FadeIn(banda))
        
        # Protagonista pensando (en la zona segura izquierda)
        prota = protagonista(
            pos=DOWN * 1.0 + LEFT * 3.0,
            playera="azul",
            altura=2.5,
            expresion="pensando"
        )
        self.play(FadeIn(prota))
        self.wait(1.0)
        
        # Efecto de nube mental (burbujas de pensamiento)
        c1 = Circle(radius=0.1, color=INK, fill_opacity=0.2).move_to(LEFT * 1.8 + UP * 0.7)
        c2 = Circle(radius=0.18, color=INK, fill_opacity=0.2).move_to(LEFT * 0.8 + UP * 1.1)
        c3 = Circle(radius=0.28, color=INK, fill_opacity=0.2).move_to(RIGHT * 0.2 + UP * 1.4)
        
        self.play(Create(c1), run_time=0.3)
        self.play(Create(c2), run_time=0.3)
        self.play(Create(c3), run_time=0.3)
        
        # Aparición del casco vikingo imaginado
        casco = casco_vikingo(pos=RIGHT * 2.6 + UP * 0.5, escala=1.5)
        self.play(FadeIn(casco))
        
        # Etiqueta descriptiva debajo del casco
        lbl = etiqueta("¿Casco con cuernos?", pos=(2.6, -1.0), color=INK)
        self.play(Write(lbl))
        self.wait(1.5)
        
        # El protagonista cambia a expresión confundida al cuestionar el mito
        prota_confundido = cambiar_cara(prota, "confundido")
        self.play(Transform(prota, prota_confundido))
        
        # Tiempo de espera final para completar la narración
        self.wait(3.6)