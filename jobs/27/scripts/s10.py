from manim import *
from zenn_rig import *

class S10(Scene):
    def construct(self):
        # Fondo estilo papel cálido
        self.add(fondo_papel())
        
        # Título seguro en la zona superior
        titulo = titulo_seguro("Pilares de Autoridad", color=AZUL_MARINO)
        self.play(Write(titulo))
        
        # Protagonista en la izquierda, señalando hacia la derecha
        prota = protagonista(
            pos=DOWN * 1.2 + LEFT * 3.8,
            playera="verde",
            altura=2.5,
            expresion="decidido",
            pose="senalando"
        )
        
        # Dos lápidas que representan los pilares de autoridad caídos
        lapida_aristoteles = lapida(
            texto="ARISTÓTELES",
            pos=RIGHT * 1.0 + DOWN * 0.8,
            ancho=2.1
        )
        
        lapida_iglesia = lapida(
            texto="LA IGLESIA",
            pos=RIGHT * 4.2 + DOWN * 0.8,
            ancho=2.1
        )
        
        # Animación de entrada del personaje
        self.play(FadeIn(prota, target_position=DOWN * 1.2 + LEFT * 4.5))
        self.wait(0.5)
        
        # Revelar los pilares de autoridad uno a uno
        self.play(FadeIn(lapida_aristoteles, shift=UP * 0.5))
        self.play(FadeIn(lapida_iglesia, shift=UP * 0.5))
        self.wait(0.5)
        
        # Resaltar la importancia con acentos rojos sobre las lápidas
        acento1 = red_accent(lapida_aristoteles, scale=1.3)
        acento2 = red_accent(lapida_iglesia, scale=1.3)
        
        self.play(
            Create(acento1),
            Create(acento2),
            run_time=1.5
        )
        
        # Espera final para sincronizar con la narración (total ~7 segundos)
        self.wait(2.0)