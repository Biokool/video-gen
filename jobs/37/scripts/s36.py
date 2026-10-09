from manim import *
from zenn_rig import *

class S36(Scene):
    def construct(self):
        # Fondo de papel de estilo divulgación
        self.add(fondo_papel())
        
        # Título en la zona superior segura
        titulo = banda_titulo("EL MITO VIKINGO", color=CORAL)
        self.add(titulo)
        
        # Protagonista a la izquierda señalando el mito
        prota = protagonista(
            pos=DOWN * 1.2 + LEFT * 3.0,
            playera="rosa",
            altura=2.4,
            expresion="decidido",
            pose="senalando"
        )
        
        # Elementos que representan la fuerza y ferocidad vikinga
        casco = casco_vikingo(pos=RIGHT * 2.8 + UP * 0.1, escala=1.6)
        fuego_efecto = fuego(pos=RIGHT * 2.8 + DOWN * 1.5, escala=1.3)
        lbl = etiqueta("Agresividad Visual", pos=RIGHT * 2.8 + UP * 1.4, color=AZUL_MARINO)
        
        # Secuencia de animación
        self.play(FadeIn(prota), run_time=1.5)
        self.wait(0.8)
        
        # Aparece el icónico casco con cuernos (el arquetipo)
        self.play(Create(casco), run_time=1.8)
        self.play(FadeIn(fuego_efecto), run_time=1.2)
        
        # El protagonista cambia a expresión reflexiva/sarcástica sobre el mito
        # cambiar_cara es una función que modifica el objeto, no devuelve una animación
        cambiar_cara(prota, "sarcastico")
        self.play(
            Write(lbl),
            run_time=1.5
        )
        
        self.wait(2.2)