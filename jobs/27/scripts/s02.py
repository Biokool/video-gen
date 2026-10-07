from manim import *
from zenn_rig import *

class S02(Scene):
    def construct(self):
        # 1. Inicializar fondo estilo papel de divulgación
        self.add(fondo_papel())
        
        # 2. Mostrar la tarjeta de título con la gran pregunta
        tc = title_card("¿El mayor error\ncientífico?", color=ORANGE)
        self.play(FadeIn(tc))
        self.wait(1.5)
        self.play(FadeOut(tc))
        
        # 3. Presentar al protagonista y elementos de ciencia/tiempo
        prota = protagonista(
            pos=DOWN * 1.2 + LEFT * 2.8, 
            playera=PLAYERA_NARANJA, 
            altura=2.5, 
            expresion="confundido", 
            pose="de_pie"
        )
        
        # Props que simbolizan la ciencia y el retraso en el tiempo
        reloj = reloj_pared(radius=0.9, pos=UP * 1.0 + RIGHT * 2.8, hora_3=True)
        quimica = matraz(pos=DOWN * 1.0 + RIGHT * 2.8, escala=1.0, liquido=TEAL)
        flecha = arrow(start=reloj.get_bottom(), end=quimica.get_top(), color=INK)
        
        # Animación de aparición
        self.play(
            FadeIn(prota),
            Create(reloj),
            Create(quimica)
        )
        self.play(Create(flecha))
        
        # Transición de expresión a reflexivo de forma segura usando Transform
        prota_pensando = protagonista(
            pos=DOWN * 1.2 + LEFT * 2.8, 
            playera=PLAYERA_NARANJA, 
            altura=2.5, 
            expresion="pensando", 
            pose="de_pie"
        )
        self.play(Transform(prota, prota_pensando))
        self.wait(1.5)