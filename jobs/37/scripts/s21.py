from manim import *
from zenn_rig import *

class S21(Scene):
    def construct(self):
        # 1. Fondo de papel estilo divulgación
        self.add(fondo_papel())
        
        # 2. Título seguro en la parte superior (evita colisiones)
        titulo = titulo_seguro("UN BLANCO FÁCIL", color=RED)
        self.add(titulo)
        
        # 3. Personaje principal (conductor) a la izquierda, zona segura inferior
        prota = protagonista(
            pos=DOWN * 1.0 + LEFT * 3.0, 
            playera="roja", 
            altura=2.4, 
            expresion="miedo", 
            pose="de_pie"
        )
        
        # 4. Elementos de peligro a la derecha (zona despejada)
        # Casco vikingo representa los cuernos (horns / target)
        cuernos = casco_vikingo(pos=RIGHT * 2.5 + UP * 0.6, escala=1.3)
        # Lápida representa el estorbo mortal
        muerte = lapida(texto="RIP", pos=RIGHT * 2.5 + DOWN * 1.1)
        
        # Presentación de la escena
        self.play(
            FadeIn(prota),
            FadeIn(cuernos),
            FadeIn(muerte),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Se activa el "blanco" o diana de peligro sobre los cuernos
        alerta = red_accent(cuernos, scale=1.4)
        self.play(
            FadeIn(alerta),
            run_time=0.8
        )
        
        # Reacción de retroceso y pánico del protagonista
        cambiar_cara(prota, "nervioso")
        self.play(
            prota.animate.shift(LEFT * 0.5),
            run_time=1.0
        )
        
        self.wait(1.2)