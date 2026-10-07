from manim import *
from zenn_rig import *

class S08(Scene):
    def construct(self):
        # Fondo de papel para estilo medieval/pergamino
        self.add(fondo_papel())
        
        # Banda de título superior
        banda = banda_titulo("Navegación Medieval", color=CORAL)
        self.add(banda)
        
        # Protagonista reflexivo en la zona segura izquierda
        prota = protagonista(
            pos=LEFT * 2.8 + DOWN * 1.2, 
            playera="azul", 
            altura=2.4, 
            expresion="pensando",
            pose="de_pie"
        )
        
        # Mapa costero (usando curva) en la zona derecha
        mapa = curva(pos=RIGHT * 2.5 + UP * 0.2, ancho=4.0, alto=2.2, color=INK, acento=RED)
        etiqueta_mapa = etiqueta("Línea de Costa", pos=(2.5, 1.5), color=INK, font_size=36)
        
        # Brújula simple debajo del mapa
        compass_body = Circle(radius=0.5, color=INK).move_to(RIGHT * 2.5 + DOWN * 1.3)
        compass_needle = arrow(
            start=RIGHT * 2.5 + DOWN * 1.6, 
            end=RIGHT * 2.5 + DOWN * 1.0, 
            color=RED, 
            width=6
        )
        
        # Secuencia de animación
        self.play(FadeIn(prota))
        self.wait(0.5)
        
        # Aparece el mapa costero
        self.play(
            Create(mapa),
            FadeIn(etiqueta_mapa),
            run_time=1.2
        )
        
        # Aparece la brújula de navegación
        self.play(
            Create(compass_body),
            Create(compass_needle),
            run_time=1.0
        )
        self.wait(0.5)
        
        # El protagonista gana confianza (expresión decidida señalando el mapa)
        prota_decidido = protagonista(
            pos=LEFT * 2.8 + DOWN * 1.2, 
            playera="azul", 
            altura=2.4, 
            expresion="decidido",
            pose="senalando"
        )
        
        self.play(Transform(prota, prota_decidido), run_time=0.8)
        self.wait(1.5)