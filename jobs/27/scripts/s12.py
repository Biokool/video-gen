from manim import *
from zenn_rig import *

class S12(Scene):
    def construct(self):
        # Fondo cálido estilo papel
        self.add(fondo_papel())
        
        # Título superior seguro
        banda = banda_titulo("La Verdad Indiscutible", color=AZUL_MARINO)
        self.play(FadeIn(banda))
        
        # Personaje principal (conductor) abajo a la izquierda
        prota = protagonista(
            pos=DOWN * 1.2 + LEFT * 3.2, 
            playera="verde", 
            altura=2.5, 
            expresion="confundido", 
            pose="de_pie"
        )
        
        # Representación de la universidad/monasterio a la derecha
        univ = oficina(pos=RIGHT * 3.2 + DOWN * 1.2, size=1.8)
        
        self.play(
            FadeIn(prota),
            FadeIn(univ),
            run_time=1.5
        )
        self.wait(0.5)
        
        # El libro/dogma de Ptolomeo en el centro
        libro = caja("Ptolomeo", pos=RIGHT * 0.2 + DOWN * 1.2, width=1.8)
        self.play(Create(libro))
        
        # Énfasis rojo sobre el libro (dogma incuestionable)
        accent = red_accent(libro, scale=1.4)
        self.play(FadeIn(accent))
        self.wait(0.5)
        
        # Reacción del protagonista y etiqueta de contexto
        etiq = etiqueta("Copia y Dogma", pos=RIGHT * 0.2 + UP * 1.0, color=CORAL)
        
        # cambiar_cara devuelve un VGroup, se debe animar con ReplacementTransform
        prota_pensando = cambiar_cara(prota, "pensando")
        self.play(
            ReplacementTransform(prota, prota_pensando),
            Write(etiq),
            run_time=1.2
        )
        
        self.wait(2.3)