from manim import *
from zenn_rig import *

class S11(Scene):
    def construct(self):
        # Fondo estilo papel cálido
        self.add(fondo_papel())
        
        # Título superior seguro
        titulo = banda_titulo("EL HOMBRE EN EL CENTRO", color=AZUL_MARINO)
        self.add(titulo)
        
        # Protagonista con playera verde y expresión solemne/pensativa, abajo a la izquierda
        prota = protagonista(
            pos=DOWN * 1.3 + LEFT * 3.8, 
            playera="verde", 
            altura=2.3, 
            expresion="pensando", 
            pose="de_pie"
        )
        
        # Esferas de la creación (Aristotélica/Cristiana) a la derecha
        centro_creacion = RIGHT * 2.0 + DOWN * 0.2
        circulo_externo = Circle(radius=1.8, color=AZUL_MARINO, stroke_width=3).move_to(centro_creacion)
        circulo_interno = Circle(radius=1.3, color=MOSTAZA, stroke_width=2).move_to(centro_creacion)
        
        # El ser humano en el centro de la creación
        humano = personaje(
            pos=centro_creacion, 
            cuerpo=CORAL, 
            altura=1.4, 
            expresion_tipo="feliz"
        )
        
        # Etiqueta descriptiva
        tag = etiqueta("Centro de la Creación", pos=RIGHT * 2.0 + UP * 2.1, color=INK, font_size=32)
        
        # Animación
        self.play(
            FadeIn(prota),
            run_time=1.0
        )
        
        self.play(
            Create(circulo_externo),
            Create(circulo_interno),
            run_time=1.8
        )
        
        self.play(
            FadeIn(humano),
            Write(tag),
            run_time=1.2
        )
        
        # El protagonista reacciona ante la idea
        prota_nuevo = cambiar_cara(prota.copy(), "mente_explotada")
        self.play(
            Transform(prota, prota_nuevo),
            run_time=0.8
        )
        
        self.wait(1.2)