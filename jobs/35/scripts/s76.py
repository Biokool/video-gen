from manim import *
from zenn_rig import *

class S76(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título seguro en la parte superior respetando zonas seguras
        titulo = titulo_seguro("¿Quién eres realmente?", color=INK, y=2.6, ancho_max=12.0)
        self.add(titulo)
        
        # Protagonista a la izquierda abajo
        prota = protagonista(pos=DOWN*1.5 + LEFT*3.5, playera=PLAYERA_NARANJA, altura=2.4, expresion='pensando', pose='de_pie')
        self.play(FadeIn(prota), run_time=0.8)
        
        # Elemento a la derecha: un ojo grande representando la adaptación / neurología
        ojo = ojo_grande(pos=RIGHT*3.2 + UP*0.2, escala=1.2, iris=TEAL)
        self.play(FadeIn(ojo), run_time=0.8)
        
        # Etiqueta compacta al lado del ojo (fuera de la zona de subtítulos y sin solaparse)
        et = etiqueta("Adaptación", pos=RIGHT*3.2 + DOWN*1.3, color=INK, font_size=36, ancho_max=4.0)
        self.play(Write(et), run_time=0.6)
        
        # Cambio de expresión del protagonista usando la función directa (sin ApplyMethod)
        cambiar_cara(prota, 'mente_explotada')
        self.wait(0.6)
        
        # Pausa para cumplir la duración objetivo (~12s en total con animaciones)
        self.wait(7.0)
        
        self.play(FadeOut(prota), FadeOut(ojo), FadeOut(et), FadeOut(titulo), run_time=1.0)