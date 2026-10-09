from manim import *
from zenn_rig import *

class S19(Scene):
    def construct(self):
        # Fondo estilo papel cálido
        self.add(fondo_papel())
        
        # Título seguro en la zona superior (único elemento de título de la escena)
        titulo = titulo_seguro("La Edad del Bronce", color=INK)
        self.play(Write(titulo))
        
        # Protagonista en la zona inferior izquierda (y <= -1.2, altura <= 2.6)
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.2, 
            playera="azul", 
            altura=2.4, 
            expresion="feliz", 
            pose="senalando"
        )
        
        # Prop temático en el lado derecho (casco de la Edad del Bronce / Veksø)
        casco = casco_vikingo(pos=RIGHT*2.8 + DOWN*0.8, escala=1.4)
        
        # Etiquetas de citación en el lado derecho (evitando la zona de subtítulos y < -2.4)
        cit_autor = etiqueta("Vandkilde, 2013", pos=(2.8, 1.6), color=INK)
        cit_libro = etiqueta("Oxford Handbook", pos=(2.8, 1.0), color=ORANGE)
        
        # Flecha indicadora desde el protagonista hacia la cita y el casco
        flecha = arrow(start=LEFT*1.6 + DOWN*0.5, end=RIGHT*1.2 + DOWN*0.5, color=ORANGE)
        
        # Secuencia de animación
        self.play(FadeIn(prota))
        self.play(Create(casco))
        self.play(Create(flecha))
        self.play(Write(cit_autor), Write(cit_libro))
        self.wait(1.5)
        
        # Reacción del protagonista
        cambiar_cara(prota, "sorpresa")
        self.wait(2.0)